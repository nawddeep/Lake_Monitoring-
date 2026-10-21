"""One-time import: copy readings from the old MySQL table into Supabase.

Source: MySQL `aarogya_jal_db.water_quality_telemetry` (written by bridge_server_sql.py).
Target: the `reading` table in Supabase, one row per value.

  python import_mysql_to_supabase.py --dry-run     # read and count only, write nothing
  python import_mysql_to_supabase.py               # import

Safe to run more than once: readings that already exist are skipped.

Mapping:
  ph            -> parameter "ph"                  (pH)
  temperature_c -> parameter "water_temp_c"        (°C)
  tds_ppm       -> parameter "tds_est_ppm"         (ppm, estimate from conductivity)
  depth_cm      -> parameter "surface_distance_cm" (cm, distance from sensor to water surface)
  epoch_time    -> measured_at (UTC). The IST text column is not used.
  water_quality_status / status_reasons are not imported (no water-quality verdict is stored).

Flags:
  SUSPECT  an exact 0.0 from the old .php endpoints, which stored 0.0 when a value was missing
  BAD      a pH outside 0-14
  OK       everything else (no calibration records exist yet)
"""

import argparse
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(line_buffering=True)  # show log lines immediately, even when redirected
load_dotenv(os.path.join(HERE, ".env"))

import psycopg  # noqa: E402
import pymysql  # noqa: E402
import pymysql.cursors  # noqa: E402

import lake_db  # noqa: E402

COLUMNS = {
    "ph": "ph",
    "temperature_c": "water_temp_c",
    "tds_ppm": "tds_est_ppm",
    "depth_cm": "surface_distance_cm",
}
OLD_PHP_SOURCES = {"PH_TEMP_NODE", "TDS_DEPTH_NODE", "FUSED_DUAL_NODE"}


def mysql_rows():
    conn = pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database=os.environ.get("MYSQL_DB", "aarogya_jal_db"),
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, station_id, epoch_time, ph, tds_ppm, temperature_c, depth_cm, source_device "
                "FROM water_quality_telemetry ORDER BY id"
            )
            return cur.fetchall()
    finally:
        conn.close()


def flag_for(code, value, source):
    if code == "ph" and not (0 <= value <= 14):
        return "BAD"
    if value == 0.0 and (source or "") in OLD_PHP_SOURCES:
        return "SUSPECT"
    return "OK"


def row_values(row):
    return {code: (None if row[col] is None else float(row[col])) for col, code in COLUMNS.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="read MySQL and report, write nothing")
    parser.add_argument("--batch", type=int, default=500, help="rows per transaction (default 500)")
    args = parser.parse_args()

    rows = mysql_rows()
    print(f"[MYSQL] Read {len(rows)} row(s) from water_quality_telemetry")
    if not rows:
        return
    by_station = defaultdict(list)
    for row in rows:
        by_station[(row["station_id"] or "FS_LAKE_STATION_01").strip()].append(row)

    stats = Counter()
    for row in rows:
        for code, value in row_values(row).items():
            if value is None:
                stats["null (skipped)"] += 1
            else:
                stats[flag_for(code, value, row["source_device"])] += 1
    for station, station_rows in by_station.items():
        first = datetime.fromtimestamp(min(r["epoch_time"] for r in station_rows), timezone.utc)
        last = datetime.fromtimestamp(max(r["epoch_time"] for r in station_rows), timezone.utc)
        print(f"[MYSQL] Station {station}: {len(station_rows)} row(s), {first.isoformat()} to {last.isoformat()} (UTC)")
    print("[MYSQL] Values by flag: " + ", ".join(f"{k}: {v}" for k, v in sorted(stats.items())))

    if args.dry_run:
        print("[DRY RUN] Nothing written to Supabase.")
        return

    inserted = 0
    with psycopg.connect(lake_db.database_url()) as conn:
        for station, station_rows in by_station.items():
            first = datetime.fromtimestamp(min(r["epoch_time"] for r in station_rows), timezone.utc)
            refs = lake_db.ensure_station_refs(conn, station, installed_at=first)
            for start in range(0, len(station_rows), args.batch):
                with conn.transaction(), conn.cursor() as cur:
                    for row in station_rows[start:start + args.batch]:
                        values = row_values(row)
                        flags = {code: flag_for(code, v, row["source_device"]) for code, v in values.items() if v is not None}
                        measured_at = datetime.fromtimestamp(row["epoch_time"], timezone.utc)
                        inserted += lake_db.insert_readings(cur, refs, measured_at, values, flags)
                done = min(start + args.batch, len(station_rows))
                print(f"[SUPABASE] {station}: {done}/{len(station_rows)} rows processed")
    total_values = sum(v for k, v in stats.items() if k != "null (skipped)")
    print(f"[DONE] {inserted} new reading(s) written; {total_values - inserted} already existed and were skipped.")


if __name__ == "__main__":
    main()
