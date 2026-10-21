import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, render_template_string
import pymysql
import pymysql.cursors

# ==============================================================================
# AAROGYA JAL - LIVE SENSOR MYSQL INGESTION BRIDGE (FATEH SAGAR LAKE)
# Database: MySQL Server (aarogya_jal_db) via WampServer / Localhost:3306
# User: root | Password: '' (Default WAMP / MySQL configuration)
# ==============================================================================

# Indian Standard Time (IST = UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'aarogya_jal_db',
    'autocommit': True,
    'cursorclass': pymysql.cursors.DictCursor
}

app = Flask(__name__)

def get_ist_time():
    """Return current datetime in Indian Standard Time (IST)."""
    return datetime.now(IST)

def get_mysql_conn():
    """Establish connection to MySQL server."""
    return pymysql.connect(**MYSQL_CONFIG)

def init_mysql_db():
    """Ensure database and water_quality_telemetry table exist in MySQL."""
    try:
        # First connect without selecting database to create if not exists
        init_conn = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            autocommit=True
        )
        with init_conn.cursor() as cur:
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
        init_conn.close()
        print("[MYSQL SUCCESS] Connected to MySQL Server! Database: aarogya_jal_db, Table: water_quality_telemetry")
        return True
    except Exception as e:
        print(f"[MYSQL ERROR] Could not initialize MySQL database: {e}")
        return False

def evaluate_water_quality(ph, tds, temp):
    """
    Evaluates water health based on Bureau of Indian Standards (BIS IS 10500)
    and Central Pollution Control Board (CPCB) criteria.
    """
    reasons = []
    status = "NORMAL"

    if ph is not None:
        if ph < 6.5:
            reasons.append(f"Acidic pH ({ph:.2f} < 6.5)")
            status = "WARNING"
        elif ph > 8.5:
            reasons.append(f"Alkaline pH ({ph:.2f} > 8.5)")
            status = "WARNING"

    if tds is not None:
        if tds > 1200:
            reasons.append(f"Severe TDS contamination ({tds:.1f} > 1200 ppm)")
            status = "CRITICAL"
        elif tds > 500:
            reasons.append(f"High TDS ({tds:.1f} > 500 ppm)")
            if status != "CRITICAL":
                status = "WARNING"

    if temp is not None:
        if temp > 35.0 or temp < 5.0:
            reasons.append(f"Abnormal Temperature ({temp:.1f} °C)")

    reason_str = "; ".join(reasons) if reasons else "Parameters within acceptable CPCB lake limits"
    return status, reason_str

# ------------------------------------------------------------------------------
# 1. UNIFIED 4-SENSOR ENDPOINT: Ingests all 4 parameters simultaneously into MySQL
# ------------------------------------------------------------------------------
@app.route('/api/telemetry', methods=['GET', 'POST'])
@app.route('/unified_telemetry.php', methods=['GET', 'POST'])
def handle_unified_telemetry():
    try:
        data = request.get_json(silent=True) or {}
        args = request.args

        lake_name = data.get('lakename') or args.get('lakename') or 'Fateh Sagar Lake'
        station_id = data.get('station_id') or args.get('station_id') or 'FS_LAKE_STATION_01'
        
        ph_raw = data.get('ph') or args.get('ph') or data.get('phlevel') or args.get('phlevel')
        ph_val = float(ph_raw) if ph_raw is not None else None

        tds_raw = data.get('tds') or args.get('tds') or data.get('tds_ppm') or args.get('tds_ppm')
        tds_val = float(tds_raw) if tds_raw is not None else None

        temp_raw = data.get('temperature') or args.get('temperature') or data.get('temp') or args.get('temp')
        temp_val = float(temp_raw) if temp_raw is not None else None

        depth_raw = data.get('depth') or args.get('depth') or data.get('distance') or args.get('distance')
        depth_val = float(depth_raw) if depth_raw is not None else None

        source = data.get('source_device') or args.get('source_device') or 'UNIFIED_4_SENSOR_NODE'

        now_ist = get_ist_time()
        ist_str = now_ist.strftime("%d/%m/%Y, %I:%M:%S %p IST")
        epoch = int(now_ist.timestamp())

        status, reasons = evaluate_water_quality(ph_val, tds_val, temp_val)

        conn = get_mysql_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO water_quality_telemetry 
                (station_id, lake_name, timestamp_ist, epoch_time, ph, tds_ppm, temperature_c, depth_cm, water_quality_status, status_reasons, source_device)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (station_id, lake_name, ist_str, epoch, ph_val, tds_val, temp_val, depth_val, status, reasons, source))
            inserted_id = cur.lastrowid
        conn.close()

        print(f"[MYSQL INGEST] [ID #{inserted_id}] [{ist_str}] pH={ph_val}, TDS={tds_val}ppm, Temp={temp_val}°C, Depth={depth_val}cm -> Status: {status}")

        return jsonify({
            "status": "success",
            "database": "MySQL",
            "sql_id": inserted_id,
            "timestamp_ist": ist_str,
            "data": {
                "ph": ph_val,
                "tds_ppm": tds_val,
                "temperature_c": temp_val,
                "depth_cm": depth_val,
                "health_status": status
            }
        }), 201

    except Exception as e:
        print(f"[MYSQL ERROR] Ingest error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ------------------------------------------------------------------------------
# 2. DUAL-BOARD INGEST & FUSING: Ingests from the 2 boards and merges in MySQL
# ------------------------------------------------------------------------------
@app.route('/temp_ph.php', methods=['GET', 'POST'])
def handle_temp_ph_compat():
    try:
        lake_name = request.args.get('lakename', 'Fateh Sagar Lake')
        temp_val = float(request.args.get('temperature', 0.0))
        ph_val = float(request.args.get('phlevel', 0.0))

        now_ist = get_ist_time()
        ist_str = now_ist.strftime("%d/%m/%Y, %I:%M:%S %p IST")
        epoch = int(now_ist.timestamp())

        conn = get_mysql_conn()
        with conn.cursor() as cur:
            # Check if there is a recent entry (< 15 sec ago) created by the TDS board missing pH/temp
            cur.execute("""
                SELECT id, tds_ppm, depth_cm FROM water_quality_telemetry 
                WHERE epoch_time >= %s AND ph IS NULL 
                ORDER BY id DESC LIMIT 1
            """, (epoch - 15,))
            recent = cur.fetchone()

            if recent:
                record_id = recent['id']
                status, reasons = evaluate_water_quality(ph_val, recent['tds_ppm'], temp_val)
                cur.execute("""
                    UPDATE water_quality_telemetry 
                    SET ph = %s, temperature_c = %s, water_quality_status = %s, status_reasons = %s, source_device = 'FUSED_DUAL_NODE'
                    WHERE id = %s
                """, (ph_val, temp_val, status, reasons, record_id))
                print(f"[MYSQL FUSE] [ID #{record_id}] [{ist_str}] pH={ph_val}, Temp={temp_val}°C")
                inserted_id = record_id
                resp_status = "fused"
            else:
                status, reasons = evaluate_water_quality(ph_val, None, temp_val)
                cur.execute("""
                    INSERT INTO water_quality_telemetry 
                    (station_id, lake_name, timestamp_ist, epoch_time, ph, temperature_c, water_quality_status, status_reasons, source_device)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'PH_TEMP_NODE')
                """, ('FS_LAKE_STATION_01', lake_name, ist_str, epoch, ph_val, temp_val, status, reasons))
                inserted_id = cur.lastrowid
                print(f"[MYSQL INSERT] [ID #{inserted_id}] [{ist_str}] pH={ph_val}, Temp={temp_val}°C")
                resp_status = "success"

        conn.close()
        return jsonify({"status": resp_status, "database": "MySQL", "sql_id": inserted_id, "timestamp_ist": ist_str}), 200

    except Exception as e:
        print(f"[MYSQL ERROR] temp_ph: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/tds_depth.php', methods=['GET', 'POST'])
def handle_tds_depth_compat():
    try:
        lake_name = request.args.get('lakename', 'Fateh Sagar Lake')
        tds_val = float(request.args.get('tds', 0.0))
        depth_val = float(request.args.get('depth', 0.0))

        now_ist = get_ist_time()
        ist_str = now_ist.strftime("%d/%m/%Y, %I:%M:%S %p IST")
        epoch = int(now_ist.timestamp())

        conn = get_mysql_conn()
        with conn.cursor() as cur:
            # Check if there is a recent entry (< 15 sec ago) created by pH board missing TDS
            cur.execute("""
                SELECT id, ph, temperature_c FROM water_quality_telemetry 
                WHERE epoch_time >= %s AND tds_ppm IS NULL 
                ORDER BY id DESC LIMIT 1
            """, (epoch - 15,))
            recent = cur.fetchone()

            if recent:
                record_id = recent['id']
                status, reasons = evaluate_water_quality(recent['ph'], tds_val, recent['temperature_c'])
                cur.execute("""
                    UPDATE water_quality_telemetry 
                    SET tds_ppm = %s, depth_cm = %s, water_quality_status = %s, status_reasons = %s, source_device = 'FUSED_DUAL_NODE'
                    WHERE id = %s
                """, (tds_val, depth_val, status, reasons, record_id))
                print(f"[MYSQL FUSE] [ID #{record_id}] [{ist_str}] TDS={tds_val}ppm, Depth={depth_val}cm")
                inserted_id = record_id
                resp_status = "fused"
            else:
                status, reasons = evaluate_water_quality(None, tds_val, None)
                cur.execute("""
                    INSERT INTO water_quality_telemetry 
                    (station_id, lake_name, timestamp_ist, epoch_time, tds_ppm, depth_cm, water_quality_status, status_reasons, source_device)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'TDS_DEPTH_NODE')
                """, ('FS_LAKE_STATION_01', lake_name, ist_str, epoch, tds_val, depth_val, status, reasons))
                inserted_id = cur.lastrowid
                print(f"[MYSQL INSERT] [ID #{inserted_id}] [{ist_str}] TDS={tds_val}ppm, Depth={depth_val}cm")
                resp_status = "success"

        conn.close()
        return jsonify({"status": resp_status, "database": "MySQL", "sql_id": inserted_id, "timestamp_ist": ist_str}), 200

    except Exception as e:
        print(f"[MYSQL ERROR] tds_depth: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# ------------------------------------------------------------------------------
# 3. QUERY APIs: Fetch Latest & History from MySQL
# ------------------------------------------------------------------------------
@app.route('/api/sql/latest', methods=['GET'])
def get_latest_mysql():
    try:
        conn = get_mysql_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
        conn.close()
        if row:
            return jsonify(row), 200
        return jsonify({"message": "No MySQL records found yet"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/sql/records', methods=['GET'])
def get_all_mysql_records():
    try:
        limit = int(request.args.get('limit', 50))
        conn = get_mysql_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
        conn.close()
        return jsonify({"count": len(rows), "records": rows, "database": "MySQL (aarogya_jal_db)"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ------------------------------------------------------------------------------
# 4. DASHBOARD UI: Live Clean Minimal Dark Interface for MySQL
# ------------------------------------------------------------------------------
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aarogya Jal - MySQL Telemetry Hub</title>
  <style>
    :root {
      --bg-main: #0d0c10;
      --card-bg: rgba(255, 255, 255, 0.03);
      --card-border: rgba(255, 255, 255, 0.08);
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --accent-safe: #10b981;
      --accent-warn: #f59e0b;
      --accent-danger: #ef4444;
      --accent-blue: #3b82f6;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
    body { background-color: var(--bg-main); color: var(--text-main); padding: 24px; min-height: 100vh; }
    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--card-border); padding-bottom: 16px; margin-bottom: 24px; }
    .title-group h1 { font-size: 1.6rem; font-weight: 600; letter-spacing: -0.5px; }
    .title-group p { font-size: 0.85rem; color: var(--text-muted); margin-top: 4px; }
    .badge-ist { background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #60a5fa; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; }
    .badge-mysql { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; margin-right: 8px; }
    
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
    .stat-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 8px; padding: 16px; }
    .stat-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }
    .stat-value { font-size: 1.8rem; font-weight: 700; margin-top: 8px; color: #fff; }
    .stat-sub { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }

    .table-container { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 8px; overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
    th { background: rgba(255, 255, 255, 0.02); padding: 12px 16px; font-weight: 600; color: var(--text-muted); border-bottom: 1px solid var(--card-border); }
    td { padding: 12px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.04); }
    tr:hover { background: rgba(255, 255, 255, 0.02); }

    .pill { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
    .pill-safe { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .pill-warn { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .pill-danger { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    .status-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; font-size: 0.8rem; color: var(--text-muted); }
    .refresh-indicator { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981; margin-right: 6px; }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h1>Aarogya Jal - MySQL Telemetry Hub</h1>
      <p>Fateh Sagar Lake Water Surveillance | MySQL: <code>aarogya_jal_db.water_quality_telemetry</code></p>
    </div>
    <div>
      <span class="badge-mysql">MySQL: CONNECTED</span>
      <span class="badge-ist" id="liveClock">IST Clock Loading...</span>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-title">pH Level</div>
      <div class="stat-value" id="cardPh">--</div>
      <div class="stat-sub">CPCB Target: 6.5 - 8.5</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">TDS (Total Solids)</div>
      <div class="stat-value" id="cardTds">-- <span style="font-size:1rem;font-weight:400;">ppm</span></div>
      <div class="stat-sub">CPCB Target: &lt; 500 ppm</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">Water Temperature</div>
      <div class="stat-value" id="cardTemp">-- <span style="font-size:1rem;font-weight:400;">°C</span></div>
      <div class="stat-sub">DS18B20 Submerged</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">Lake Depth / Clearance</div>
      <div class="stat-value" id="cardDepth">-- <span style="font-size:1rem;font-weight:400;">cm</span></div>
      <div class="stat-sub">HC-SR04 Ultrasonic</div>
    </div>
  </div>

  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>MySQL ID #</th>
          <th>IST Timestamp</th>
          <th>pH</th>
          <th>TDS (ppm)</th>
          <th>Temp (°C)</th>
          <th>Depth (cm)</th>
          <th>Status</th>
          <th>Analysis</th>
          <th>Source</th>
        </tr>
      </thead>
      <tbody id="telemetryBody">
        <tr><td colspan="9" style="text-align:center; padding: 24px; color: var(--text-muted);">Polling MySQL database...</td></tr>
      </tbody>
    </table>
  </div>

  <div class="status-bar">
    <div><span class="refresh-indicator"></span> Live MySQL Polling active (Every 2 seconds)</div>
    <div id="recordCount">Total Records: 0</div>
  </div>

  <script>
    function updateClock() {
      const now = new Date();
      document.getElementById('liveClock').textContent = now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata' }) + ' IST';
    }
    setInterval(updateClock, 1000);
    updateClock();

    async function fetchMySQLData() {
      try {
        const res = await fetch('/api/sql/records?limit=25');
        const data = await res.json();
        const records = data.records || [];

        document.getElementById('recordCount').textContent = `Showing last ${records.length} records in MySQL (aarogya_jal_db)`;

        if (records.length > 0) {
          const latest = records[0];
          document.getElementById('cardPh').textContent = latest.ph !== null ? latest.ph.toFixed(2) : '--';
          document.getElementById('cardTds').innerHTML = (latest.tds_ppm !== null ? latest.tds_ppm.toFixed(1) : '--') + ' <span style="font-size:1rem;font-weight:400;">ppm</span>';
          document.getElementById('cardTemp').innerHTML = (latest.temperature_c !== null ? latest.temperature_c.toFixed(1) : '--') + ' <span style="font-size:1rem;font-weight:400;">°C</span>';
          document.getElementById('cardDepth').innerHTML = (latest.depth_cm !== null ? latest.depth_cm.toFixed(1) : '--') + ' <span style="font-size:1rem;font-weight:400;">cm</span>';

          const tbody = document.getElementById('telemetryBody');
          tbody.innerHTML = records.map(r => {
            let pillClass = 'pill-safe';
            if (r.water_quality_status === 'WARNING') pillClass = 'pill-warn';
            if (r.water_quality_status === 'CRITICAL') pillClass = 'pill-danger';

            return `
              <tr>
                <td><strong>#${r.id}</strong></td>
                <td>${r.timestamp_ist}</td>
                <td>${r.ph !== null ? r.ph.toFixed(2) : '-'}</td>
                <td>${r.tds_ppm !== null ? r.tds_ppm.toFixed(1) : '-'}</td>
                <td>${r.temperature_c !== null ? r.temperature_c.toFixed(1) : '-'}</td>
                <td>${r.depth_cm !== null ? r.depth_cm.toFixed(1) : '-'}</td>
                <td><span class="pill ${pillClass}">${r.water_quality_status}</span></td>
                <td style="color:var(--text-muted); font-size:0.8rem;">${r.status_reasons || '-'}</td>
                <td style="font-size:0.75rem; color:#34d399;">${r.source_device}</td>
              </tr>
            `;
          }).join('');
        }
      } catch (err) {
        console.error('Fetch error:', err);
      }
    }

    fetchMySQLData();
    setInterval(fetchMySQLData, 2000);
  </script>
</body>
</html>
"""

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

if __name__ == "__main__":
    print("[INFO] Initializing Aarogya Jal MySQL Bridge Server...")
    if init_mysql_db():
        print(f"[INFO] Indian Standard Time (IST): {get_ist_time().strftime('%d/%m/%Y, %I:%M:%S %p IST')}")
        print("[SERVER] Starting MySQL Server on http://0.0.0.0:5000...")
        print("[SERVER] Web Dashboard available at: http://localhost:5000/dashboard")
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        print("[FATAL] Could not connect to MySQL server on 127.0.0.1:3306. Check WampServer.")
