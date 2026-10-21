-- =============================================================================
-- AAROGYA JAL - SMART WATER QUALITY MONITORING SYSTEM (FATEH SAGAR LAKE)
-- Relational SQL Database Schema (Compatible with SQLite, MySQL & PostgreSQL)
-- =============================================================================

CREATE TABLE IF NOT EXISTS water_quality_telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id VARCHAR(50) NOT NULL DEFAULT 'FS_LAKE_STATION_01',
    lake_name VARCHAR(100) NOT NULL DEFAULT 'Fateh Sagar Lake',
    timestamp_ist VARCHAR(50) NOT NULL,            -- e.g. "12/10/2026, 10:30:15 AM IST"
    epoch_time INTEGER NOT NULL,                   -- Unix epoch seconds for range queries
    ph REAL DEFAULT NULL,                          -- pH level (0 - 14)
    tds_ppm REAL DEFAULT NULL,                     -- Total Dissolved Solids in parts per million
    temperature_c REAL DEFAULT NULL,               -- Water Temperature in Celsius
    depth_cm REAL DEFAULT NULL,                    -- Water Surface Clearance / Depth in cm
    water_quality_status VARCHAR(30) DEFAULT 'NORMAL', -- NORMAL, WARNING, CRITICAL
    status_reasons VARCHAR(255) DEFAULT '',        -- Human-readable reason for alert (e.g. "Low pH; High TDS")
    source_device VARCHAR(50) DEFAULT 'UNIFIED_NODE'
);

-- Index for high-speed chronological querying
CREATE INDEX IF NOT EXISTS idx_telemetry_time ON water_quality_telemetry (epoch_time DESC);
CREATE INDEX IF NOT EXISTS idx_telemetry_station ON water_quality_telemetry (station_id);

-- Sample Query: Fetch latest 10 readings
-- SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT 10;

-- Sample Query: Identify contamination anomalies (CPCB Indian Water Standards)
-- SELECT * FROM water_quality_telemetry 
-- WHERE ph < 6.5 OR ph > 8.5 OR tds_ppm > 500
-- ORDER BY epoch_time DESC;
