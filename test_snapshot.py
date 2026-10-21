import json
import os
import pymysql
import pymysql.cursors
from datetime import datetime, timezone

SEED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lake_dashboard", "tests", "fixtures", "seed.json")

def generate_snapshot(limit=100):
    with open(SEED_FILE, "r") as f:
        snapshot = json.load(f)

    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="aarogya_jal_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT %s", (limit,))
        rows = cur.fetchall()
    conn.close()

    readings = []
    derived = []
    cycles = []
    latest_map = {}

    for r in reversed(rows):
        epoch = r["epoch_time"]
        iso_time = datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. pH (Sensor 1, Controller 1)
        if r["ph"] is not None:
            rid = r["id"] * 10 + 1
            reading = {
                "reading_id": rid,
                "sensor_id": 1,
                "controller_id": 1,
                "measured_at": iso_time,
                "device_time_raw": None,
                "received_at": iso_time,
                "raw_value": float(r["ph"]),
                "raw_unit": "pH",
                "corrected_value": float(r["ph"]),
                "corrected_unit": "pH",
                "calibration_id": None,
                "is_synthetic": False,
                "quality_flag": "OK" if 6.5 <= r["ph"] <= 8.5 else "OUT_OF_RANGE",
                "flags": []
            }
            readings.append(reading)
            latest_map[1] = reading

        # 2. Temperature (Sensor 2, Controller 1)
        if r["temperature_c"] is not None:
            rid = r["id"] * 10 + 2
            reading = {
                "reading_id": rid,
                "sensor_id": 2,
                "controller_id": 1,
                "measured_at": iso_time,
                "device_time_raw": None,
                "received_at": iso_time,
                "raw_value": float(r["temperature_c"]),
                "raw_unit": "°C",
                "corrected_value": float(r["temperature_c"]),
                "corrected_unit": "°C",
                "calibration_id": None,
                "is_synthetic": False,
                "quality_flag": "OK" if r["temperature_c"] > 0 else "OUT_OF_RANGE",
                "flags": []
            }
            readings.append(reading)
            latest_map[2] = reading

        # 3. TDS (Sensor 3, Controller 2)
        if r["tds_ppm"] is not None:
            rid = r["id"] * 10 + 3
            reading = {
                "reading_id": rid,
                "sensor_id": 3,
                "controller_id": 2,
                "measured_at": iso_time,
                "device_time_raw": None,
                "received_at": iso_time,
                "raw_value": float(r["tds_ppm"]),
                "raw_unit": "ppm",
                "corrected_value": float(r["tds_ppm"]),
                "corrected_unit": "ppm",
                "calibration_id": None,
                "is_synthetic": False,
                "quality_flag": "OK" if r["tds_ppm"] <= 500 else "OUT_OF_RANGE",
                "flags": []
            }
            readings.append(reading)
            latest_map[3] = reading

            # Derived TDS measurement
            derived.append({
                "derived_id": rid,
                "source_reading_id": rid,
                "temp_reading_id": r["id"] * 10 + 2 if r["temperature_c"] is not None else None,
                "temp_age_s": 0,
                "kind": "tds_est_mg_l",
                "value": float(r["tds_ppm"]),
                "unit": "mg/L",
                "method_note": "Gravity TDS curve",
                "quality_flag": "OK",
                "measured_at": iso_time
            })

        # 4. Water Level (Sensor 4, Controller 2)
        if r["depth_cm"] is not None:
            rid = r["id"] * 10 + 4
            reading = {
                "reading_id": rid,
                "sensor_id": 4,
                "controller_id": 2,
                "measured_at": iso_time,
                "device_time_raw": None,
                "received_at": iso_time,
                "raw_value": round(float(r["depth_cm"]) / 100.0, 3),
                "raw_unit": "m",
                "corrected_value": round(float(r["depth_cm"]) / 100.0, 3),
                "corrected_unit": "m",
                "calibration_id": None,
                "is_synthetic": False,
                "quality_flag": "OK",
                "flags": []
            }
            readings.append(reading)
            latest_map[4] = reading

        # Measurement Cycle
        cycles.append({
            "cycle_id": r["id"],
            "cycle_start": iso_time,
            "tolerance_s": 30,
            "ph_reading_id": r["id"] * 10 + 1 if r["ph"] is not None else None,
            "temp_reading_id": r["id"] * 10 + 2 if r["temperature_c"] is not None else None,
            "tds_reading_id": r["id"] * 10 + 3 if r["tds_ppm"] is not None else None,
            "level_reading_id": r["id"] * 10 + 4 if r["depth_cm"] is not None else None,
            "max_skew_s": 2,
            "complete": bool(r["ph"] is not None and r["tds_ppm"] is not None)
        })

    snapshot["readings"] = readings
    snapshot["derived_measurements"] = derived
    snapshot["measurement_cycles"] = cycles
    snapshot["latest"] = list(latest_map.values())
    snapshot["meta"]["source"] = "mysql_live"
    snapshot["meta"]["total_rows_in_db"] = len(rows)

    return snapshot

if __name__ == "__main__":
    s = generate_snapshot(5)
    print("Snapshot generated successfully!")
    print("Readings count:", len(s["readings"]))
    print("Latest count:", len(s["latest"]))
    print("Sample reading:", json.dumps(s["readings"][0], indent=2))
