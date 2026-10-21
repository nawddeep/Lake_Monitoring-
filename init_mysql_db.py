import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='')
with conn.cursor() as cur:
    cur.execute("CREATE DATABASE IF NOT EXISTS aarogya_jal_db;")
    cur.execute("USE aarogya_jal_db;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS water_quality_telemetry (
            id INT AUTO_INCREMENT PRIMARY KEY,
            station_id VARCHAR(50) NOT NULL DEFAULT 'FS_LAKE_STATION_01',
            lake_name VARCHAR(100) NOT NULL DEFAULT 'Fateh Sagar Lake',
            timestamp_ist VARCHAR(50) NOT NULL,
            epoch_time BIGINT NOT NULL,
            ph FLOAT DEFAULT NULL,
            tds_ppm FLOAT DEFAULT NULL,
            temperature_c FLOAT DEFAULT NULL,
            depth_cm FLOAT DEFAULT NULL,
            water_quality_status VARCHAR(30) DEFAULT 'NORMAL',
            status_reasons VARCHAR(255) DEFAULT '',
            source_device VARCHAR(50) DEFAULT 'FUSED_DUAL_NODE',
            INDEX idx_time (epoch_time)
        );
    """)
    conn.commit()
    print("[SUCCESS] aarogya_jal_db database and water_quality_telemetry table created in MySQL!")
conn.close()
