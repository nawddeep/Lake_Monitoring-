import os
import sys
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# ==============================================================================
# AAROGYA JAL - MONGODB ATLAS LIVE TELEMETRY CONNECTION
# ==============================================================================

# Your MongoDB Atlas Connection URI
MONGO_URI = "mongodb+srv://ramanimanan13_db_user:manman@cluster0.lqinmlj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Target Database and Collection Name
DATABASE_NAME = "aarogya_jal_db"
COLLECTION_NAME = "live_water_telemetry"

def get_database_client(uri: str):
    """Establishes a connection to MongoDB Atlas with a timeout check."""
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    return client

def insert_telemetry_reading(db, reading_data: dict):
    """Inserts a new live sensor data packet into the database."""
    collection = db[COLLECTION_NAME]
    if "timestamp" not in reading_data:
        reading_data["timestamp"] = datetime.now(timezone.utc)
    result = collection.insert_one(reading_data)
    print(f"[SUCCESS] Data packet inserted successfully with ID: {result.inserted_id}")
    return result.inserted_id

def get_latest_reading(db):
    """Fetches the most recent live data packet from the lake station."""
    collection = db[COLLECTION_NAME]
    latest = collection.find_one(sort=[("timestamp", -1)])
    return latest

if __name__ == "__main__":
    print("[INFO] Connecting to MongoDB Atlas Cluster0...")
    try:
        client = get_database_client(MONGO_URI)
        print("[SUCCESS] Connected successfully to MongoDB Atlas!")
        
        db = client[DATABASE_NAME]
        
        # Sample live incoming reading from Fateh Sagar Lake Station
        sample_packet = {
            "station_id": "FS_LAKE_STATION_01",
            "location": "Fateh Sagar Lake, Udaipur",
            "timestamp": datetime.now(timezone.utc),
            "metrics": {
                "ph": 7.42,
                "electrical_conductivity_uS_cm": 420.5,
                "dissolved_oxygen_mg_L": 6.85,
                "dissolved_oxygen_sat_percent": 91.2,
                "turbidity_ntu": 4.1,
                "temperature_surface_c": 24.3,
                "temperature_deep_c": 22.8,
                "water_level_m": 3.82,
                "battery_voltage_v": 13.2,
                "battery_soc_percent": 94
            },
            "status": "NORMAL",
            "anomalies_detected": []
        }
        
        # Insert packet
        inserted_id = insert_telemetry_reading(db, sample_packet)
        
        # Retrieve packet
        latest = get_latest_reading(db)
        print("\n--- Latest Live Data in Database ---")
        print(f"Station: {latest.get('station_id')}")
        print(f"Time: {latest.get('timestamp')}")
        print(f"pH: {latest['metrics']['ph']}, EC: {latest['metrics']['electrical_conductivity_uS_cm']} uS/cm, DO: {latest['metrics']['dissolved_oxygen_mg_L']} mg/L")
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"[ERROR] Connection failed: {e}")
        print("\n[NOTE] Ensure your IP address is whitelisted in MongoDB Atlas:")
        print("1. Go to cloud.mongodb.com -> Security / Network Access")
        print("2. Click 'Add IP Address' -> Select 'Allow Access from Anywhere' (0.0.0.0/0)")
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")
