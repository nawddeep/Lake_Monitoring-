# Sensor bridge → Supabase

Python scripts that move sensor data into the app's Supabase database (the `reading` table and
friends, defined in `prisma/schema.prisma`).

| File                          | What it does                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `supabase_bridge.py`          | Receives readings from the ESP nodes and stores them in Supabase. Replaces `bridge_server_sql.py` (MySQL) and `bridge_server.py` (MongoDB). |
| `import_mysql_to_supabase.py` | One-time copy of the existing MySQL rows into Supabase. Safe to re-run.                                                                     |
| `lake_db.py`                  | Shared database code used by both.                                                                                                          |

The ESP firmware does not need to change: the bridge serves the same endpoints on the same port
(`/api/telemetry`, `/unified_telemetry.php`, `/temp_ph.php`, `/tds_depth.php`).

## Setup (once)

Python 3.9 or newer.

```bash
cd bridge
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # Windows: copy .env.example .env
```

Edit `bridge/.env` and set `DATABASE_URL` to the Supabase **session pooler** string you were sent
privately (port 5432). `bridge/.env` is gitignored: never commit it, never paste it in chat.
Use the **dev** project's string until everything is checked; production comes last.

## 1. Import the old MySQL data (once)

With WampServer/MySQL running on this laptop:

```bash
python import_mysql_to_supabase.py --dry-run   # shows row counts and date range, writes nothing
python import_mysql_to_supabase.py             # copies into Supabase
```

Running it again later only adds rows that aren't there yet.

What gets copied: pH, water temperature, TDS (stored as _Estimated TDS from conductivity_) and the
ultrasonic distance (stored as _distance from sensor to water surface_, not water depth). Times come
from `epoch_time` and are stored in UTC. The `water_quality_status` / `status_reasons` columns are
**not** copied: the app does not grade water quality from four sensors.

Flags: an exact `0.0` from the old `.php` endpoints is marked `SUSPECT` (those endpoints stored 0.0
when a value was missing), a pH outside 0–14 is `BAD`, everything else is `OK`.

## 2. Run the new bridge

Stop the old bridge first (both use port 5000), then:

```bash
python supabase_bridge.py
```

Check it: open `http://localhost:5000/health` (should show `"database": "ok"`) and, after a sensor
posts, `http://localhost:5000/api/latest`.

- Each value is stored as its own row, stamped with the time the bridge received it (UTC).
- Missing values are skipped, never stored as 0.
- If Supabase can't be reached (hotspot down), readings are saved in `bridge/spool.jsonl` and sent
  automatically with the next successful request. `/health` shows how many are waiting.
- Only stations listed in `ALLOWED_STATIONS` are accepted.
- Optional: set `INGEST_TOKEN` and have the firmware send it as `X-Ingest-Token` (or `?token=`) so
  other devices on the network can't post fake readings.

## Running on Vercel (the `bridge` service)

`vercel.json` deploys this folder as the `bridge` service next to the Next.js app, on the same
domain. Public paths: `/api/telemetry`, `/unified_telemetry.php`, `/temp_ph.php`, `/tds_depth.php`
and `/api/bridge/health`, `/api/bridge/latest`. Everything else goes to the app.

- On Vercel the endpoints are public, so **ingest is refused unless `INGEST_TOKEN` is set** in the
  Vercel environment, and the boards must send it (`X-Ingest-Token` header or `?token=`).
- It uses the project's shared `DATABASE_URL` (Supabase transaction pooler, port 6543);
  prepared statements are disabled for that.
- The spool file lives in `/tmp` there and is temporary.
- The boards must post to `https://<your-domain>/...`. Vercel serves HTTPS only, so the ESP
  firmware needs a TLS-capable client (for example `WiFiClientSecure` on ESP8266/ESP32).

## Security

- Database passwords, Wi-Fi passwords and API keys go in `bridge/.env` (or the firmware's local
  config), never in committed code. Earlier commits exposed a MongoDB Atlas password, Wi-Fi
  passwords and a ThingSpeak key; those must be changed at the source.
- The bridge has no login of its own; run it only on a trusted network.
