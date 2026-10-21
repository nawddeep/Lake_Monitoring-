import os
import sys
import json
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from pymongo import MongoClient

# ==============================================================================
# AAROGYA JAL - LIVE SENSOR TO MONGODB ATLAS INGESTION BRIDGE (EXPLICIT IST)
# ==============================================================================

# Indian Standard Time (IST = UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

MONGO_URI = "mongodb+srv://ramanimanan13_db_user:manman@cluster0.lqinmlj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "aarogya_jal_db"
COLLECTION_NAME = "live_water_telemetry"
CACHE_FILE = "local_telemetry_cache.json"

app = Flask(__name__)

mongo_client = None
telemetry_col = None

def init_mongo():
    global mongo_client, telemetry_col
    try:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        mongo_client.admin.command('ping')
        db = mongo_client[DATABASE_NAME]
        telemetry_col = db[COLLECTION_NAME]
        print("[SUCCESS] Connected to MongoDB Atlas successfully!")
        flush_cache()
        return True
    except Exception as e:
        print(f"[WARNING] MongoDB Atlas not reachable yet: {e}")
        return False

def get_ist_time():
    return datetime.now(IST)

def save_document(doc):
    global telemetry_col
    if telemetry_col is None:
        init_mongo()

    if telemetry_col is not None:
        try:
            result = telemetry_col.insert_one(doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"[ERROR] Insert failed, caching locally: {e}")

    # Fallback: Save to local cache
    cache = []
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
        except Exception:
            cache = []

    cache.append(doc)

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"[CACHE] Saved reading to local cache ({len(cache)} readings buffered)")
    return "cached_locally"

def flush_cache():
    global telemetry_col
    if telemetry_col is not None and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached = json.load(f)
            if cached:
                print(f"[SYNC] Flushing {len(cached)} cached readings to MongoDB Atlas...")
                for item in cached:
                    telemetry_col.insert_one(item)
                os.remove(CACHE_FILE)
                print("[SYNC] All cached readings successfully synced to Atlas!")
        except Exception as e:
            print(f"[SYNC ERROR] Failed to flush cache: {e}")

# ------------------------------------------------------------------------------
# 1. Endpoint for Program 1 (pH + Temperature)
# ------------------------------------------------------------------------------
@app.route('/temp_ph.php', methods=['GET', 'POST'])
def handle_temp_ph():
    try:
        lake_name = request.args.get('lakename', 'Fateh Sagar Lake')
        temp_val = float(request.args.get('temperature', 0.0))
        ph_val = float(request.args.get('phlevel', 0.0))

        now_ist = get_ist_time()
        ist_str = now_ist.strftime("%d/%m/%Y, %I:%M:%S %p IST")

        doc = {
            "station_id": "FS_LAKE_STATION_01",
            "lake_name": lake_name,
            "sensor_type": "PH_TEMP_BOARD",
            "timestamp": ist_str,                     # Plain String in MongoDB Atlas: "10/10/2026, 12:43:00 PM IST"
            "timestamp_iso": now_ist.isoformat(),     # ISO format: "2026-10-10T12:43:00.123+05:30"
            "metrics": {
                "ph": ph_val,
                "temperature_c": temp_val
            },
            "status": "NORMAL" if (6.5 <= ph_val <= 8.5) else "ALERT"
        }

        doc_id = save_document(doc)
        print(f"[INGEST] [{ist_str}] pH: {ph_val}, Temp: {temp_val} C -> ID: {doc_id}")
        return jsonify({"status": "success", "id": doc_id, "timestamp": ist_str}), 200

    except Exception as e:
        print(f"[ERROR] Ingest error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ------------------------------------------------------------------------------
# 2. Endpoint for Program 2 (TDS + Ultrasonic Depth)
# ------------------------------------------------------------------------------
@app.route('/tds_depth.php', methods=['GET', 'POST'])
def handle_tds_depth():
    try:
        lake_name = request.args.get('lakename', 'Fateh Sagar Lake')
        tds_val = float(request.args.get('tds', 0.0))
        depth_val = float(request.args.get('depth', 0.0))

        now_ist = get_ist_time()
        ist_str = now_ist.strftime("%d/%m/%Y, %I:%M:%S %p IST")

        doc = {
            "station_id": "FS_LAKE_STATION_01",
            "lake_name": lake_name,
            "sensor_type": "TDS_DEPTH_BOARD",
            "timestamp": ist_str,                     # Plain String in MongoDB Atlas: "10/10/2026, 12:43:00 PM IST"
            "timestamp_iso": now_ist.isoformat(),     # ISO format: "2026-10-10T12:43:00.123+05:30"
            "metrics": {
                "tds_ppm": tds_val,
                "distance_depth_cm": depth_val
            },
            "status": "NORMAL" if (tds_val <= 500.0) else "WARNING"
        }

        doc_id = save_document(doc)
        print(f"[INGEST] [{ist_str}] TDS: {tds_val} ppm, Depth: {depth_val} cm -> ID: {doc_id}")
        return jsonify({"status": "success", "id": doc_id, "timestamp": ist_str}), 200

    except Exception as e:
        print(f"[ERROR] Ingest error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ------------------------------------------------------------------------------
# 3. View Latest Reading
# ------------------------------------------------------------------------------
@app.route('/api/telemetry/latest', methods=['GET'])
def get_latest():
    global telemetry_col
    if telemetry_col is not None:
        try:
            latest = telemetry_col.find_one(sort=[("_id", -1)])
            if latest:
                latest["_id"] = str(latest["_id"])
                return jsonify(latest), 200
        except Exception:
            pass

    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
            if cache:
                return jsonify(cache[-1]), 200
        except Exception:
            pass

    return jsonify({"message": "No data available yet"}), 404

if __name__ == "__main__":
    print("[INFO] Initializing Aarogya Jal Ingestion Bridge...")
    init_mongo()
    print(f"[INFO] Indian Standard Time (IST): {get_ist_time().strftime('%d/%m/%Y, %I:%M:%S %p IST')}")
    print("[SERVER] Starting Bridge Server on http://0.0.0.0:5000...")
    print("[SERVER] ESP8266 boards can now send live data!")
    app.run(host="0.0.0.0", port=5000, debug=False)
