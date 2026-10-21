"""Shared Supabase/PostgreSQL helpers for the bridge server and the MySQL importer.

Writes into the lake tables defined in prisma/schema.prisma (site, station, sensor,
sensor_installation, parameter, reading). All times are stored in UTC.

Nothing here prints connection strings or passwords.
"""

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

# The four channels the sensor nodes send. Codes are stable identifiers used in the
# `parameter` table; names and units are what the dashboard shows.
PARAMETERS = {
    "ph": ("pH", "pH"),
    "water_temp_c": ("Water temperature", "°C"),
    # A conductivity-based estimate, not a laboratory TDS measurement.
    "tds_est_ppm": ("Estimated TDS (from conductivity)", "ppm"),
    # The ultrasonic sensor measures the distance down to the water surface, not water depth.
    "surface_distance_cm": ("Distance from sensor to water surface", "cm"),
}

PLACEHOLDER_SENSOR_NOTE = (
    "Serial number not recorded: placeholder created by the bridge/importer. "
    "Probe make and model not verified."
)


def _env(name, default):
    return lambda: os.environ.get(name, default)


@dataclass
class Config:
    organization_name: str = field(default_factory=_env("LAKE_ORG_NAME", "Aarogya Jal"))
    organization_slug: str = field(default_factory=_env("LAKE_ORG_SLUG", "aarogya-jal"))
    site_name: str = field(default_factory=_env("LAKE_SITE_NAME", "Fateh Sagar Lake"))


@dataclass
class StationRefs:
    station_id: str
    sensor_ids: dict = field(default_factory=dict)  # parameter code -> sensor id
    parameter_ids: dict = field(default_factory=dict)  # parameter code -> parameter id


def database_url():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is not set. Put it in bridge/.env (see bridge/.env.example).")
    return url


def _organization_id(cur, cfg):
    cur.execute("SELECT id FROM organization WHERE slug = %s", (cfg.organization_slug,))
    row = cur.fetchone()
    if row:
        return row[0]
    org_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO organization (id, name, slug, created_at, updated_at) VALUES (%s, %s, %s, now(), now())",
        (org_id, cfg.organization_name, cfg.organization_slug),
    )
    print(f"[SETUP] Created organization '{cfg.organization_name}' ({cfg.organization_slug})")
    return org_id


def _site_id(cur, organization_id, cfg):
    cur.execute(
        "SELECT id FROM site WHERE organization_id = %s AND name = %s", (organization_id, cfg.site_name)
    )
    row = cur.fetchone()
    if row:
        return row[0]
    site_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO site (id, organization_id, name) VALUES (%s, %s, %s)",
        (site_id, organization_id, cfg.site_name),
    )
    print(f"[SETUP] Created site '{cfg.site_name}'")
    return site_id


def _station_id(cur, site_id, station_name):
    cur.execute("SELECT id FROM station WHERE site_id = %s AND name = %s", (site_id, station_name))
    row = cur.fetchone()
    if row:
        return row[0]
    station_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO station (id, site_id, name, kind) VALUES (%s, %s, %s, 'PHYSICAL')",
        (station_id, site_id, station_name),
    )
    print(f"[SETUP] Created station '{station_name}'")
    return station_id


def _parameter_ids(cur):
    for code, (name, unit) in PARAMETERS.items():
        cur.execute(
            "INSERT INTO parameter (code, name, unit) VALUES (%s, %s, %s) ON CONFLICT (code) DO NOTHING",
            (code, name, unit),
        )
    cur.execute("SELECT code, id FROM parameter WHERE code = ANY(%s)", (list(PARAMETERS),))
    return dict(cur.fetchall())


def _sensor_id(cur, station_id, station_name, code, installed_at):
    serial = f"{station_name}-{code}"
    cur.execute(
        "INSERT INTO sensor (id, serial_number, notes) VALUES (%s, %s, %s) ON CONFLICT (serial_number) DO NOTHING",
        (str(uuid.uuid4()), serial, PLACEHOLDER_SENSOR_NOTE),
    )
    cur.execute("SELECT id FROM sensor WHERE serial_number = %s", (serial,))
    sensor_id = cur.fetchone()[0]
    cur.execute(
        "SELECT 1 FROM sensor_installation WHERE sensor_id = %s AND station_id = %s AND removed_at IS NULL",
        (sensor_id, station_id),
    )
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO sensor_installation (id, sensor_id, station_id, installed_at) VALUES (%s, %s, %s, %s)",
            (str(uuid.uuid4()), sensor_id, station_id, installed_at),
        )
    return sensor_id


def ensure_station_refs(conn, station_name, cfg=None, installed_at=None):
    """Find (or create once) everything a reading for `station_name` needs."""
    cfg = cfg or Config()
    installed_at = installed_at or datetime.now(timezone.utc)
    with conn.transaction(), conn.cursor() as cur:
        organization_id = _organization_id(cur, cfg)
        site_id = _site_id(cur, organization_id, cfg)
        station_id = _station_id(cur, site_id, station_name)
        parameter_ids = _parameter_ids(cur)
        sensor_ids = {
            code: _sensor_id(cur, station_id, station_name, code, installed_at) for code in PARAMETERS
        }
    return StationRefs(station_id=str(station_id), sensor_ids=sensor_ids, parameter_ids=parameter_ids)


def insert_readings(cur, refs, measured_at, values, flags=None):
    """Insert one row per non-null value. Returns how many were new (duplicates are skipped).

    values: {parameter code: float or None}; flags: {parameter code: 'OK'|'SUSPECT'|'BAD'}.
    """
    flags = flags or {}
    rows = [
        (refs.station_id, refs.sensor_ids[code], refs.parameter_ids[code], measured_at, value, flags.get(code, "OK"))
        for code, value in values.items()
        if value is not None
    ]
    inserted = 0
    for row in rows:
        cur.execute(
            """
            INSERT INTO reading (station_id, sensor_id, parameter_id, measured_at, value, flag)
            VALUES (%s, %s, %s, %s, %s, %s::reading_flag)
            ON CONFLICT (sensor_id, parameter_id, measured_at) DO NOTHING
            """,
            row,
        )
        inserted += cur.rowcount
    return inserted
