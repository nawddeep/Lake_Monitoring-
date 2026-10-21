import bridge_server_sql
import json

bridge_server_sql.init_sql_db()
client = bridge_server_sql.app.test_client()

# 1. Test Unified Ingest
resp = client.post('/api/telemetry', json={
    'station_id': 'FS_LAKE_STATION_01',
    'lakename': 'Fateh Sagar Lake',
    'ph': 7.65,
    'tds': 310.2,
    'temperature': 25.4,
    'depth': 142.0,
    'source_device': 'UNIFIED_TEST'
})
print('Unified POST status:', resp.status_code)
print('Unified POST body:', resp.get_json())

# 2. Test Dual Ingest Fusing
resp_ph = client.get('/temp_ph.php?temperature=26.1&phlevel=7.80')
print('Temp/pH GET:', resp_ph.status_code, resp_ph.get_json())

resp_tds = client.get('/tds_depth.php?tds=325.0&depth=138.5')
print('TDS/Depth GET (Fused):', resp_tds.status_code, resp_tds.get_json())

# 3. Test SQL Record Query
resp_records = client.get('/api/sql/records?limit=5')
records = resp_records.get_json()['records']
print('\nRecent SQL Records Count:', len(records))
for r in records:
    print(f"  Row #{r['id']}: pH={r['ph']}, TDS={r['tds_ppm']}ppm, Temp={r['temperature_c']}C, Depth={r['depth_cm']}cm, Time={r['timestamp_ist']}, Status={r['water_quality_status']}")
