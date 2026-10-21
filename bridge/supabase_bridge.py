"""Aarogya Jal sensor bridge: receives readings from the ESP nodes and stores them in Supabase.

Replaces bridge_server_sql.py (MySQL) and bridge_server.py (MongoDB). The ESP firmware does
not need to change: the same endpoints are served on the same port.

  POST/GET /api/telemetry          all four values (also /unified_telemetry.php)
  POST/GET /temp_ph.php            ?temperature=..&phlevel=..
  POST/GET /tds_depth.php          ?tds=..&depth=..
  GET      /health                 bridge and database status
  GET      /api/latest             latest stored value per parameter

Each value becomes one row in the `reading` table, stamped with the time the bridge received
it (UTC). Missing values are skipped, never stored as 0. No water-quality verdict is computed.
If Supabase is unreachable, readings are written to a local spool file and sent later.

Configuration comes from bridge/.env (see bridge/.env.example). Run:  python supabase_bridge.py
"""

import json
import os
import sys
import threading
from datetime import datetime, timezone

from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(line_buffering=True)  # show log lines immediately, even when redirected
load_dotenv(os.path.join(HERE, ".env"))

from flask import Flask, jsonify, request  # noqa: E402
from psycopg_pool import ConnectionPool  # noqa: E402

import lake_db  # noqa: E402

STATION_NAME = os.environ.get("STATION_NAME", "FS_LAKE_STATION_01")
ALLOWED_STATIONS = {
    s.strip() for s in os.environ.get("ALLOWED_STATIONS", STATION_NAME).split(",") if s.strip()
}
INGEST_TOKEN = os.environ.get("INGEST_TOKEN", "")
SPOOL_PATH = os.environ.get("SPOOL_PATH", os.path.join(HERE, "spool.jsonl"))
PORT = int(os.environ.get("PORT", "5000"))
DB_TIMEOUT_S = float(os.environ.get("DB_TIMEOUT_S", "5"))  # give up quickly and spool if Supabase is down

app = Flask(__name__)
pool = ConnectionPool(
    lake_db.database_url(), min_size=1, max_size=4, open=False,
    kwargs={"autocommit": True, "connect_timeout": 10}
)
_refs_cache = {}
_refs_lock = threading.Lock()
_spool_lock = threading.Lock()


def refs_for(station_name):
    with _refs_lock:
        if station_name not in _refs_cache:
            with pool.connection(timeout=DB_TIMEOUT_S) as conn:
                _refs_cache[station_name] = lake_db.ensure_station_refs(conn, station_name)
        return _refs_cache[station_name]


def to_float(*candidates):
    """First candidate that is present and numeric; None if none are."""
    for value in candidates:
        if value is None or value == "":
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
    return None


def write(station_name, measured_at, values):
    refs = refs_for(station_name)
    with pool.connection(timeout=DB_TIMEOUT_S) as conn, conn.cursor() as cur:
        return lake_db.insert_readings(cur, refs, measured_at, values)


def spool(station_name, measured_at, values):
    with _spool_lock, open(SPOOL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"station": station_name, "measured_at": measured_at.isoformat(), "values": values}) + "\n")


def flush_spool():
    """Send readings saved while Supabase was unreachable. Keeps any that still fail."""
    with _spool_lock:
        if not os.path.exists(SPOOL_PATH):
            return 0
        with open(SPOOL_PATH, encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
        os.remove(SPOOL_PATH)
    sent, failed = 0, []
    for line in lines:
        item = json.loads(line)
        try:
            sent += write(item["station"], datetime.fromisoformat(item["measured_at"]), item["values"])
        except Exception:
            failed.append(line)
    if failed:
        with _spool_lock, open(SPOOL_PATH, "a", encoding="utf-8") as f:
            f.writelines(failed)
    if lines:
        print(f"[SPOOL] Sent {sent} saved reading(s); {len(failed)} line(s) still waiting")
    return sent


def store(station_name, values):
    if station_name not in ALLOWED_STATIONS:
        return jsonify({"status": "error", "message": f"Unknown station '{station_name}'"}), 400
    if all(v is None for v in values.values()):
        return jsonify({"status": "error", "message": "No sensor values in request"}), 400
    measured_at = datetime.now(timezone.utc)
    try:
        stored = write(station_name, measured_at, values)
    except Exception as e:  # network or database outage: keep the reading locally
        spool(station_name, measured_at, values)
        print(f"[SPOOLED] {station_name} {measured_at.isoformat()} {values} ({type(e).__name__})")
        return jsonify({"status": "spooled", "database": "Supabase", "measured_at_utc": measured_at.isoformat()}), 202
    flush_spool()
    print(f"[STORED] {station_name} {measured_at.isoformat()} {values} -> {stored} new row(s)")
    return jsonify({
        "status": "success",
        "database": "Supabase",
        "station": station_name,
        "measured_at_utc": measured_at.isoformat(),
        "stored": {k: v for k, v in values.items() if v is not None},
    }), 201


def authorised():
    if not INGEST_TOKEN:
        return True
    return INGEST_TOKEN in (request.headers.get("X-Ingest-Token"), request.args.get("token"))


def payload():
    return (request.get_json(silent=True) or {}), request.args


def unauthorised():
    return jsonify({"status": "error", "message": "Invalid ingest token"}), 401


@app.route("/api/telemetry", methods=["GET", "POST"])
@app.route("/unified_telemetry.php", methods=["GET", "POST"])
def unified_telemetry():
    if not authorised():
        return unauthorised()
    data, args = payload()

    def pick(*keys):
        return [src.get(k) for k in keys for src in (data, args)]

    station = str(data.get("station_id") or args.get("station_id") or STATION_NAME).strip()
    return store(station, {
        "ph": to_float(*pick("ph", "phlevel")),
        "water_temp_c": to_float(*pick("temperature", "temp")),
        "tds_est_ppm": to_float(*pick("tds", "tds_ppm")),
        "surface_distance_cm": to_float(*pick("depth", "distance")),
    })


@app.route("/temp_ph.php", methods=["GET", "POST"])
def temp_ph():
    if not authorised():
        return unauthorised()
    data, args = payload()
    return store(STATION_NAME, {
        "ph": to_float(args.get("phlevel"), data.get("phlevel"), args.get("ph"), data.get("ph")),
        "water_temp_c": to_float(args.get("temperature"), data.get("temperature")),
    })


@app.route("/tds_depth.php", methods=["GET", "POST"])
def tds_depth():
    if not authorised():
        return unauthorised()
    data, args = payload()
    return store(STATION_NAME, {
        "tds_est_ppm": to_float(args.get("tds"), data.get("tds")),
        "surface_distance_cm": to_float(args.get("depth"), data.get("depth")),
    })


@app.route("/health")
def health():
    try:
        with pool.connection(timeout=10) as conn:
            conn.execute("SELECT 1")
        db = "ok"
    except Exception as e:
        db = f"unreachable ({type(e).__name__})"
    waiting = 0
    if os.path.exists(SPOOL_PATH):
        with open(SPOOL_PATH, encoding="utf-8") as f:
            waiting = sum(1 for line in f if line.strip())
    return jsonify({"bridge": "ok", "database": db, "station": STATION_NAME, "spooled_requests": waiting})


@app.route("/api/latest")
def latest():
    station = request.args.get("station_id", STATION_NAME)
    with pool.connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT DISTINCT ON (p.code) p.code, p.name, p.unit, r.value, r.flag::text, r.measured_at
            FROM reading r
            JOIN parameter p ON p.id = r.parameter_id
            JOIN station s ON s.id = r.station_id
            WHERE s.name = %s
            ORDER BY p.code, r.measured_at DESC
            """,
            (station,),
        )
        rows = cur.fetchall()
    return jsonify({
        "station": station,
        "readings": [
            {"parameter": c, "name": n, "unit": u, "value": v, "flag": f, "measured_at_utc": t.isoformat()}
            for c, n, u, v, f, t in rows
        ],
    })


if __name__ == "__main__":
    pool.open(wait=False)
    print(f"[BRIDGE] Station {STATION_NAME} | allowed stations: {', '.join(sorted(ALLOWED_STATIONS))}")
    print(f"[BRIDGE] Ingest token: {'required' if INGEST_TOKEN else 'not required (set INGEST_TOKEN to require one)'}")
    print(f"[BRIDGE] Listening on http://0.0.0.0:{PORT}  (health: /health)")
    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)
