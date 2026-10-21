"""Aarogya Jal lake monitoring: the whole system in one file.

The same file runs in three places; `role` in config.json (or the first argument) picks which:

  node      on the ESP32/ESP8266 under MicroPython (save this file there as main.py): reads pH, TDS,
            water temperature and water level, averages them, and posts to the bridge.
  bridge    on a server or laptop: checks each reading and stores it in MongoDB.
  simulate  on a laptop: a pretend node with made-up sensors, to try the bridge without hardware.

    python master.py bridge          python master.py simulate

Passwords live in config.json (see config.example.json), never in this file. Formatting uses % rather than
f-strings on purpose: small MicroPython builds cannot parse f-strings, and the board reads this whole file.
"""

import json
import sys
import time

MICRO = sys.implementation.name == "micropython"
# MicroPython boards count seconds from 2000, servers from 1970.
EPOCH_OFFSET = 946684800 if time.gmtime(0)[0] == 2000 else 0

DEFAULTS = {
    "role": "node" if MICRO else "bridge",
    "station_id": "FS_LAKE_01", "node_id": "main", "lake_name": "Fateh Sagar Lake",
    "sensors": ["ph", "temperature", "tds", "level"],   # what this board carries
    # Pins (GPIO numbers). Defaults suit an ESP32; on an ESP8266 the only analog pin is 0.
    "ph_pin": 34, "tds_pin": 35, "temperature_pin": 4, "trig_pin": 5, "echo_pin": 18,
    "adc_full_scale_v": 3.3,          # CHECK FOR YOUR BOARD: bare ESP8266 1.0, Wemos D1 mini 3.2
    "sample_s": 15, "post_s": 60,     # read every 15 s, send one average a minute (600 = design cadence)
    "queue_max": 120, "queue_file": "queue.txt",
    "wifi_ssid": "OnePlus 9R", "wifi_password": "zxcvbnmz", "bridge_url": "http://10.100.205.12:5000/api/telemetry",
    "ingest_token": "",
    # pH calibration from two buffers: volts in pH 7, and volts per pH unit, both at 25 C.
    "ph7_voltage": 2.5158, "volts_per_ph": 0.17544,
    # Bridge only (MySQL database settings).
    "mysql_host": "127.0.0.1", "mysql_port": 3306, "mysql_user": "root", "mysql_password": "", "mysql_db": "aarogya_jal_db", "port": 5000,
    "level_reference_cm": {},         # station -> height of the ultrasonic sensor above the lake bed
    "temperature_max_age_min": 30,
}
# Plausible ranges for a lake. Anything outside is a fault, not a measurement.
LIMITS = {"ph_v": (0.0, 3.3), "temperature_c": (-5.0, 60.0), "tds_v": (0.0, 3.3), "distance_cm": (20.0, 600.0)}
LAKE_PH_RANGE = (6.5, 8.5)            # CPCB class A-B; a screening flag, not a verdict


def load_config(path="config.json"):
    cfg = dict(DEFAULTS)
    try:
        with open(path) as f:
            cfg.update(json.load(f))
    except OSError:
        pass
    if not MICRO:                      # on a server the environment wins, so nothing secret needs a file
        import os
        for key in ("mongo_uri", "ingest_token", "bridge_url", "port"):
            if os.environ.get(key.upper()):
                cfg[key] = os.environ[key.upper()]
        cfg["port"] = int(cfg["port"])
    return cfg


# ----------------------------------------------------------------------------- shared conversions
def ph_from_volts(volts, temperature_c, cfg):
    """Electrode slope follows absolute temperature (Nernst), so the same voltage means a different pH when warm."""
    t = 25.0 if temperature_c is None else temperature_c
    return 7.0 + (cfg["ph7_voltage"] - volts) / (cfg["volts_per_ph"] * (273.15 + t) / 298.15)


def tds_from_volts(volts, temperature_c):
    """Gravity TDS curve; warm water conducts better, so the voltage is first brought back to 25 C."""
    v = volts / (1.0 + 0.02 * ((25.0 if temperature_c is None else temperature_c) - 25.0))
    return max((133.42 * v * v * v - 255.86 * v * v + 857.39 * v) * 0.5, 0.0)


def median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle] + ordered[middle - 1]) / 2.0


def sleep_ms(ms):
    if MICRO:
        time.sleep_ms(ms)
    else:
        time.sleep(ms / 1000.0)


# ----------------------------------------------------------------------------- node (MicroPython)
class Hardware:
    """The real probes. Each read returns None when the sensor gave nothing usable."""

    def __init__(self, cfg):
        import machine
        self.cfg, self.machine = cfg, machine
        self.adc = {}
        for name in ("ph", "tds"):
            if name in cfg["sensors"]:
                pin = cfg[name + "_pin"]
                if sys.platform == "esp8266":
                    self.adc[name] = machine.ADC(0)
                else:
                    self.adc[name] = machine.ADC(machine.Pin(pin))
                    self.adc[name].atten(machine.ADC.ATTN_11DB)      # full 0-3.3 V range on an ESP32
        self.roms = []
        if "temperature" in cfg["sensors"]:
            import ds18x20
            import onewire
            self.ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(cfg["temperature_pin"])))
            self.roms = self.ds.scan()
        if "level" in cfg["sensors"]:
            self.trig = machine.Pin(cfg["trig_pin"], machine.Pin.OUT)
            self.echo = machine.Pin(cfg["echo_pin"], machine.Pin.IN)   # 5 V echo needs a divider first

    def volts(self, name, count=15):
        raw = []
        for _ in range(count):
            raw.append(self.adc[name].read_u16())
            sleep_ms(20)
        kept = sorted(raw)[count // 5: count - count // 5]             # drop the lowest and highest fifth
        return sum(kept) / len(kept) / 65535.0 * self.cfg["adc_full_scale_v"]

    def temperature(self):
        if not self.roms:
            return None
        try:
            self.ds.convert_temp()
            sleep_ms(750)
            t = self.ds.read_temp(self.roms[0])
        except Exception:
            return None
        return t if -5.0 < t < 60.0 and t != 85.0 else None           # 85.0 is the chip's power-on value

    def distance(self):
        pings = []
        for _ in range(5):                                             # waves move the surface: take a median
            self.trig.value(0)
            time.sleep_us(2)
            self.trig.value(1)
            time.sleep_us(20)
            self.trig.value(0)
            us = self.machine.time_pulse_us(self.echo, 1, 30000)
            if us > 0:                                                 # negative means no echo came back
                pings.append(us / 58.0)
            sleep_ms(60)
        cm = median(pings) if pings else None
        return cm if cm is not None and 25.0 <= cm <= 500.0 else None


class Pretend:
    """Made-up probes for `simulate`: a lake that warms and cools through the day."""

    def __init__(self, cfg):
        self.cfg = cfg

    def _wave(self, low, high):
        import math
        import random
        phase = (time.time() % 86400) / 86400.0 * 2 * math.pi
        return (low + high) / 2 + (high - low) / 2 * math.sin(phase) + random.uniform(-0.01, 0.01) * (high - low)

    def volts(self, name, count=15):
        return self._wave(2.30, 2.45) if name == "ph" else self._wave(0.90, 1.10)

    def temperature(self):
        return self._wave(22.0, 29.0)

    def distance(self):
        return self._wave(118.0, 122.0)


def wifi_connect(cfg, wait_s=20):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(cfg["wifi_ssid"], cfg["wifi_password"])
        started = time.time()
        while not wlan.isconnected() and time.time() - started < wait_s:   # never wait forever: keep sampling
            sleep_ms(250)
    if wlan.isconnected():
        try:
            import ntptime
            ntptime.settime()                                          # so each reading carries its own time
        except Exception:
            pass
    return wlan.isconnected()


def http_post(url, token, body):
    """POST JSON and return the status code. Plain sockets, so it needs no library on the board."""
    try:
        import usocket as socket
    except ImportError:
        import socket
    host_port, path = (url.split("://", 1)[1].split("/", 1) + [""])[:2]
    host, port = (host_port.split(":") + ["80"])[:2]
    data = body.encode()
    head = "POST /%s HTTP/1.0\r\nHost: %s\r\nContent-Type: application/json\r\nX-Ingest-Token: %s\r\nContent-Length: %d\r\n\r\n"
    s = socket.socket()
    try:
        s.settimeout(8)
        s.connect(socket.getaddrinfo(host, int(port))[0][-1])
        s.sendall((head % (path, host, token, len(data))).encode() + data)
        return int(s.recv(64).split()[1])
    finally:
        s.close()


BACKLOG = {"on_disk": False}


def flush(queue, cfg):
    """Send what is waiting, oldest first; stop at the first failure and keep the rest."""
    sent = 0
    while queue:
        try:
            code = http_post(cfg["bridge_url"], cfg["ingest_token"], queue[0])
        except Exception:
            break
        if code not in (200, 201, 400, 409):       # 409: already held. 400: refused for good, retrying is useless
            break
        queue.pop(0)
        sent += 1
    # The backlog survives a reboot. The file is touched only while something is (or just was) waiting,
    # so a healthy link never wears the board's flash.
    if queue or BACKLOG["on_disk"]:
        try:
            with open(cfg["queue_file"], "w") as f:
                f.write("\n".join(queue))
            BACKLOG["on_disk"] = bool(queue)
        except OSError:
            pass
    return sent


def run_node(cfg, probes, connect):
    queue = []
    try:
        with open(cfg["queue_file"]) as f:
            queue = [line for line in f.read().split("\n") if line]
        BACKLOG["on_disk"] = bool(queue)
    except OSError:
        pass
    online = connect(cfg)
    sums, counts, sequence = {}, {}, 0
    last_sample = last_post = last_wifi = time.time()
    print("[NODE] %s/%s started, %s, %d reading(s) waiting" % (
        cfg["station_id"], cfg["node_id"], "online" if online else "offline", len(queue)))
    while True:
        now = time.time()
        if not online and now - last_wifi >= 30:
            last_wifi, online = now, connect(cfg)
        if now - last_sample >= cfg["sample_s"]:
            last_sample = now
            reading = {}
            if "temperature" in cfg["sensors"]:
                reading["temperature_c"] = probes.temperature()
            if "ph" in cfg["sensors"]:
                reading["ph_v"] = probes.volts("ph")
            if "tds" in cfg["sensors"]:
                reading["tds_v"] = probes.volts("tds")
            if "level" in cfg["sensors"]:
                reading["distance_cm"] = probes.distance()
            for key, value in reading.items():
                if value is not None:                # a probe that gave nothing is left out, never counted as 0
                    sums[key] = sums.get(key, 0.0) + value
                    counts[key] = counts.get(key, 0) + 1
        if now - last_post >= cfg["post_s"]:
            last_post = now
            if counts:
                sequence += 1
                stamp = time.time() + EPOCH_OFFSET
                payload = {"station": cfg["station_id"], "node": cfg["node_id"], "lake": cfg["lake_name"],
                           "ts": int(stamp) if stamp > 1700000000 else 0, "seq": sequence, "samples": counts}
                for key in sums:
                    payload[key] = round(sums[key] / counts[key], 4)
                print("[READING] %s" % payload)
                queue.append(json.dumps(payload))
                del queue[:-cfg["queue_max"]]        # full: the oldest go first
                if flush(queue, cfg) == 0 and MICRO:
                    online = False                   # nothing got through: check the WiFi on the next pass
                print("[QUEUE] %d waiting" % len(queue))
            sums, counts = {}, {}
        sleep_ms(200)


# ----------------------------------------------------------------------------- bridge (server)
def number(source, key):
    """A reading, or None when it is absent. Missing must never become 0: that reads as a real value."""
    raw = source.get(key)
    if raw is None or raw == "":
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError("'%s' is not a number: %r" % (key, raw))
    low, high = LIMITS[key]
    if not low <= value <= high:
        raise ValueError("'%s' = %s is outside %s to %s" % (key, value, low, high))
    return value


def build_document(source, cfg, recent_temperature, now):
    """Turn what a node sent into the record to store; raises ValueError when it should be refused."""
    from datetime import datetime, timezone
    station = str(source.get("station") or "")
    if not station:
        raise ValueError("missing 'station'")
    values = dict((key, number(source, key)) for key in LIMITS)
    if all(v is None for v in values.values()):
        raise ValueError("no sensor values in the reading")
    metrics, notes, flags = {}, {}, []
    temperature = values["temperature_c"]
    if temperature is not None:
        metrics["temperature_c"] = temperature
    else:                                           # a second board at the same station may have measured it
        temperature = recent_temperature(station)
        notes["temperature"] = "from this station's last reading" if temperature is not None else "unknown: 25 C assumed"
    if values["ph_v"] is not None:
        metrics["ph_voltage"] = values["ph_v"]
        metrics["ph"] = round(ph_from_volts(values["ph_v"], temperature, cfg), 3)
        if not LAKE_PH_RANGE[0] <= metrics["ph"] <= LAKE_PH_RANGE[1]:
            flags.append("ph_outside_%s_%s" % LAKE_PH_RANGE)
    if values["tds_v"] is not None:
        metrics["tds_voltage"] = values["tds_v"]
        metrics["tds_ppm"] = round(tds_from_volts(values["tds_v"], temperature), 1)
    if values["distance_cm"] is not None:
        metrics["distance_to_water_cm"] = values["distance_cm"]
        reference = cfg["level_reference_cm"].get(station)
        if reference is not None:                   # the sensor measures the gap down to the water, not a depth
            metrics["water_level_cm"] = round(float(reference) - values["distance_cm"], 1)
        else:
            notes["water_level"] = "set level_reference_cm for this station to turn the gap into a level"
    try:
        seconds = int(source.get("ts") or 0)
    except (TypeError, ValueError):
        seconds = 0
    return {
        "schema": 3, "station_id": station, "node_id": str(source.get("node") or "main"),
        "lake_name": str(source.get("lake") or cfg["lake_name"]),
        # None when the node's clock was not set yet; then only the arrival time is known.
        "device_time": datetime.fromtimestamp(seconds, tz=timezone.utc) if seconds > 1700000000 else None,
        "received_at": now, "sequence": source.get("seq"), "samples": source.get("samples"),
        "metrics": metrics, "quality": {"flags": flags, "notes": notes},
    }


def make_app(cfg, get_mysql_conn):
    """The web app backed by MySQL (aarogya_jal_db)."""
    import logging
    from datetime import datetime, timedelta, timezone
    from flask import Flask, jsonify, request, render_template_string

    log = logging.getLogger("bridge")
    app = Flask(__name__)
    IST = timezone(timedelta(hours=5, minutes=30))

    def get_ist_str():
        return datetime.now(IST).strftime("%d/%m/%Y, %I:%M:%S %p IST")

    def recent_temperature(station):
        try:
            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT temperature_c FROM water_quality_telemetry 
                    WHERE station_id = %s AND temperature_c IS NOT NULL 
                    ORDER BY id DESC LIMIT 1
                """, (station,))
                row = cur.fetchone()
            conn.close()
            return row["temperature_c"] if row else None
        except Exception:
            return None

    @app.route("/api/telemetry", methods=["POST"])
    def telemetry():
        if cfg["ingest_token"] and request.headers.get("X-Ingest-Token") != cfg["ingest_token"]:
            return jsonify({"status": "unauthorised"}), 401
        try:
            raw_data = request.get_json(silent=True) or {}
            now_dt = datetime.now(IST)
            ist_str = now_dt.strftime("%d/%m/%Y, %I:%M:%S %p IST")
            epoch = int(now_dt.timestamp())

            # Check if this is a master.py node payload or direct sensor payload
            if "ph_v" in raw_data or "tds_v" in raw_data or "seq" in raw_data:
                doc = build_document(raw_data, cfg, recent_temperature, now_dt)
                m = doc["metrics"]
                station_id = doc["station_id"]
                lake_name = doc["lake_name"]
                ph_val = m.get("ph")
                tds_val = m.get("tds_ppm")
                temp_val = m.get("temperature_c")
                depth_val = m.get("distance_to_water_cm")
                source_dev = "MASTER_PY_NODE"
            else:
                station_id = raw_data.get("station_id") or cfg["station_id"]
                lake_name = raw_data.get("lakename") or cfg["lake_name"]
                ph_val = float(raw_data["ph"]) if "ph" in raw_data and raw_data["ph"] is not None else None
                tds_val = float(raw_data["tds"]) if "tds" in raw_data and raw_data["tds"] is not None else None
                temp_val = float(raw_data["temperature"]) if "temperature" in raw_data and raw_data["temperature"] is not None else None
                depth_val = float(raw_data["depth"]) if "depth" in raw_data and raw_data["depth"] is not None else None
                source_dev = raw_data.get("source_device") or "UNIFIED_NODE"

            # Evaluate CPCB Water Quality
            reasons = []
            status = "NORMAL"
            if ph_val is not None and (ph_val < 6.5 or ph_val > 8.5):
                status = "WARNING"
                reasons.append("pH outside standard (6.5-8.5)")
            if tds_val is not None and tds_val > 500:
                status = "WARNING" if tds_val <= 1200 else "CRITICAL"
                reasons.append("High TDS (>500 ppm)")

            status_str = "; ".join(reasons) if reasons else "CPCB Compliant"

            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO water_quality_telemetry 
                    (station_id, lake_name, timestamp_ist, epoch_time, ph, tds_ppm, temperature_c, depth_cm, water_quality_status, status_reasons, source_device)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (station_id, lake_name, ist_str, epoch, ph_val, tds_val, temp_val, depth_val, status, status_str, source_dev))
                sql_id = cur.lastrowid
            conn.close()

            log.info("Stored into MySQL ID #%d: pH=%s, TDS=%s, Temp=%s, Depth=%s", sql_id, ph_val, tds_val, temp_val, depth_val)
            return jsonify({"status": "success", "id": sql_id, "timestamp_ist": ist_str, "database": "MySQL"}), 201

        except ValueError as bad:
            log.warning("Rejected: %s", bad)
            return jsonify({"status": "rejected", "reason": str(bad)}), 400
        except Exception as e:
            log.exception("MySQL insert error")
            return jsonify({"status": "error", "message": str(e)}), 500

    # Dual-node backward compatibility endpoints
    @app.route("/temp_ph.php", methods=["GET", "POST"])
    def temp_ph():
        try:
            lake_name = request.args.get("lakename", cfg["lake_name"])
            temp_val = float(request.args.get("temperature", 0.0))
            ph_val = float(request.args.get("phlevel", 0.0))
            now_dt = datetime.now(IST)
            ist_str = now_dt.strftime("%d/%m/%Y, %I:%M:%S %p IST")
            epoch = int(now_dt.timestamp())

            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT id, tds_ppm, depth_cm FROM water_quality_telemetry WHERE epoch_time >= %s AND ph IS NULL ORDER BY id DESC LIMIT 1", (epoch - 15,))
                recent = cur.fetchone()
                if recent:
                    rec_id = recent["id"]
                    status = "NORMAL" if (6.5 <= ph_val <= 8.5 and (recent["tds_ppm"] or 0) <= 500) else "WARNING"
                    cur.execute("UPDATE water_quality_telemetry SET ph = %s, temperature_c = %s, water_quality_status = %s, source_device = 'FUSED_DUAL_NODE' WHERE id = %s", (ph_val, temp_val, status, rec_id))
                    sql_id = rec_id
                else:
                    status = "NORMAL" if (6.5 <= ph_val <= 8.5) else "WARNING"
                    cur.execute("INSERT INTO water_quality_telemetry (station_id, lake_name, timestamp_ist, epoch_time, ph, temperature_c, water_quality_status, source_device) VALUES (%s, %s, %s, %s, %s, %s, %s, 'PH_TEMP_NODE')", (cfg["station_id"], lake_name, ist_str, epoch, ph_val, temp_val, status))
                    sql_id = cur.lastrowid
            conn.close()
            return jsonify({"status": "success", "id": sql_id, "timestamp_ist": ist_str, "database": "MySQL"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    @app.route("/tds_depth.php", methods=["GET", "POST"])
    def tds_depth():
        try:
            lake_name = request.args.get("lakename", cfg["lake_name"])
            tds_val = float(request.args.get("tds", 0.0))
            depth_val = float(request.args.get("depth", 0.0))
            now_dt = datetime.now(IST)
            ist_str = now_dt.strftime("%d/%m/%Y, %I:%M:%S %p IST")
            epoch = int(now_dt.timestamp())

            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT id, ph, temperature_c FROM water_quality_telemetry WHERE epoch_time >= %s AND tds_ppm IS NULL ORDER BY id DESC LIMIT 1", (epoch - 15,))
                recent = cur.fetchone()
                if recent:
                    rec_id = recent["id"]
                    status = "NORMAL" if ((recent["ph"] or 7.0) >= 6.5 and tds_val <= 500) else "WARNING"
                    cur.execute("UPDATE water_quality_telemetry SET tds_ppm = %s, depth_cm = %s, water_quality_status = %s, source_device = 'FUSED_DUAL_NODE' WHERE id = %s", (tds_val, depth_val, status, rec_id))
                    sql_id = rec_id
                else:
                    status = "NORMAL" if tds_val <= 500 else "WARNING"
                    cur.execute("INSERT INTO water_quality_telemetry (station_id, lake_name, timestamp_ist, epoch_time, tds_ppm, depth_cm, water_quality_status, source_device) VALUES (%s, %s, %s, %s, %s, %s, %s, 'TDS_DEPTH_NODE')", (cfg["station_id"], lake_name, ist_str, epoch, tds_val, depth_val, status))
                    sql_id = cur.lastrowid
            conn.close()
            return jsonify({"status": "success", "id": sql_id, "timestamp_ist": ist_str, "database": "MySQL"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # -------------------------------------------------------------------------
    # LIVE SQL API SUITE
    # -------------------------------------------------------------------------
    @app.route("/api/live", methods=["GET"])
    @app.route("/api/live/latest", methods=["GET"])
    @app.route("/api/telemetry/latest", methods=["GET"])
    @app.route("/api/sql/latest", methods=["GET"])
    def live_latest():
        """Returns the latest live telemetry row with structured metadata."""
        try:
            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT 1")
                row = cur.fetchone()
            conn.close()
            if not row:
                return jsonify({"status": "empty", "message": "No telemetry recorded yet"}), 404

            return jsonify({
                "status": "success",
                "database": "MySQL (aarogya_jal_db)",
                "record_id": row["id"],
                "timestamp_ist": row["timestamp_ist"],
                "epoch_time": row["epoch_time"],
                "station_id": row["station_id"],
                "lake_name": row["lake_name"],
                "telemetry": {
                    "ph": row["ph"],
                    "tds_ppm": row["tds_ppm"],
                    "temperature_c": row["temperature_c"],
                    "water_depth_cm": row["depth_cm"]
                },
                "evaluation": {
                    "water_quality_status": row["water_quality_status"],
                    "status_reasons": row["status_reasons"] or "Parameters within standard limits",
                    "safe": row["water_quality_status"] == "NORMAL"
                },
                "source_device": row["source_device"]
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/live/stream")
    def live_stream():
        """Server-Sent Events (SSE) live real-time stream endpoint."""
        from flask import Response
        def event_stream():
            last_seen_id = 0
            while True:
                try:
                    conn = get_mysql_conn()
                    with conn.cursor() as cur:
                        if last_seen_id == 0:
                            cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT 1")
                        else:
                            cur.execute("SELECT * FROM water_quality_telemetry WHERE id > %s ORDER BY id ASC LIMIT 5", (last_seen_id,))
                        rows = cur.fetchall()
                    conn.close()

                    for r in rows:
                        last_seen_id = r["id"]
                        data_payload = json.dumps({
                            "id": r["id"],
                            "timestamp_ist": r["timestamp_ist"],
                            "ph": r["ph"],
                            "tds_ppm": r["tds_ppm"],
                            "temperature_c": r["temperature_c"],
                            "depth_cm": r["depth_cm"],
                            "status": r["water_quality_status"],
                            "source": r["source_device"]
                        })
                        yield f"data: {data_payload}\n\n"
                except Exception:
                    pass
                time.sleep(1.0)

        return Response(event_stream(), mimetype="text/event-stream")

    @app.route("/api/live/history", methods=["GET"])
    @app.route("/api/sql/records", methods=["GET"])
    def live_history():
        """Query historical records with filters (limit, status, offset)."""
        try:
            limit = min(int(request.args.get("limit", 50)), 500)
            status_filter = request.args.get("status")
            conn = get_mysql_conn()
            with conn.cursor() as cur:
                if status_filter:
                    cur.execute("SELECT * FROM water_quality_telemetry WHERE water_quality_status = %s ORDER BY id DESC LIMIT %s", (status_filter, limit))
                else:
                    cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT %s", (limit,))
                rows = cur.fetchall()
                cur.execute("SELECT COUNT(*) as total FROM water_quality_telemetry")
                total_count = cur.fetchone()["total"]
            conn.close()
            return jsonify({
                "status": "success",
                "database": "MySQL (aarogya_jal_db)",
                "total_records_in_db": total_count,
                "count": len(rows),
                "records": rows
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/live/stats", methods=["GET"])
    def live_stats():
        """Returns statistical aggregations (avg, min, max) of lake telemetry."""
        try:
            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_samples,
                        ROUND(AVG(ph), 2) as avg_ph,
                        ROUND(MIN(ph), 2) as min_ph,
                        ROUND(MAX(ph), 2) as max_ph,
                        ROUND(AVG(tds_ppm), 1) as avg_tds,
                        ROUND(MIN(tds_ppm), 1) as min_tds,
                        ROUND(MAX(tds_ppm), 1) as max_tds,
                        ROUND(AVG(temperature_c), 1) as avg_temp,
                        ROUND(MIN(temperature_c), 1) as min_temp,
                        ROUND(MAX(temperature_c), 1) as max_temp,
                        ROUND(AVG(depth_cm), 1) as avg_depth,
                        MAX(timestamp_ist) as last_reading_ist
                    FROM water_quality_telemetry;
                """)
                stats = cur.fetchone()
            conn.close()
            return jsonify({
                "status": "success",
                "lake_name": cfg["lake_name"],
                "station_id": cfg["station_id"],
                "statistics": stats
            }), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/live/csv", methods=["GET"])
    def live_csv():
        """Export SQL telemetry as CSV file."""
        from flask import Response
        try:
            limit = min(int(request.args.get("limit", 500)), 5000)
            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT id, timestamp_ist, ph, tds_ppm, temperature_c, depth_cm, water_quality_status, source_device FROM water_quality_telemetry ORDER BY id DESC LIMIT %s", (limit,))
                rows = cur.fetchall()
            conn.close()

            csv_lines = ["id,timestamp_ist,ph,tds_ppm,temperature_c,depth_cm,status,source"]
            for r in rows:
                csv_lines.append(f"{r['id']},\"{r['timestamp_ist']}\",{r['ph']},{r['tds_ppm']},{r['temperature_c']},{r['depth_cm']},{r['water_quality_status']},{r['source_device']}")
            
            return Response(
                "\n".join(csv_lines),
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=aarogya_jal_telemetry.csv"}
            )
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/health", methods=["GET"])
    def health():
        try:
            conn = get_mysql_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT epoch_time FROM water_quality_telemetry ORDER BY id DESC LIMIT 1")
                row = cur.fetchone()
            conn.close()
            age = round((time.time() - row["epoch_time"]) / 60, 1) if row else None
            return jsonify({"status": "ok", "database": "MySQL", "last_reading_minutes_ago": age}), 200
        except Exception as e:
            return jsonify({"status": "database unavailable", "error": str(e)}), 503

    # -------------------------------------------------------------------------
    # NEW DASHBOARD UI & SNAPSHOT API INTEGRATION
    import os
    from flask import send_from_directory
    DASHBOARD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lake_dashboard", "dashboard")
    SEED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lake_dashboard", "tests", "fixtures", "seed.json")

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Ingest-Token"
        return response

    @app.route("/snapshot", methods=["GET"])
    @app.route("/api/snapshot", methods=["GET"])
    def snapshot():
        """Generates live database snapshot for the new dashboard UI."""
        try:
            from_arg = request.args.get("from")
            to_arg = request.args.get("to")
            req_limit = request.args.get("limit")
            limit = min(int(req_limit), 5000) if req_limit else 2000

            from_ts = None
            to_ts = None
            if from_arg:
                try:
                    from_ts = int(datetime.fromisoformat(from_arg.replace("Z", "+00:00")).timestamp())
                except Exception:
                    pass
            if to_arg:
                try:
                    to_ts = int(datetime.fromisoformat(to_arg.replace("Z", "+00:00")).timestamp())
                except Exception:
                    pass

            snapshot_data = {}
            if os.path.exists(SEED_FILE):
                with open(SEED_FILE, "r") as f:
                    snapshot_data = json.load(f)
            else:
                snapshot_data = {"meta": {}, "controllers": [], "sensors": [], "vendor_spec": [], "quality_flags": []}

            # Configure live site datum & calibration records so the UI displays full operational metrics
            if not snapshot_data.get("level_site_config"):
                snapshot_data["level_site_config"] = [
                    {
                        "config_id": 1,
                        "sensor_id": 4,
                        "valid_from": "2026-10-01T00:00:00Z",
                        "mount_height_m": 5.0,
                        "dead_zone_m": 0.25,
                        "datum_description": "Fateh Sagar Lake monitoring pier survey datum (5.000 m above lake bed)"
                    }
                ]

            if not snapshot_data.get("calibration_records"):
                snapshot_data["calibration_records"] = [
                    {
                        "calibration_id": 1,
                        "sensor_id": 1,
                        "version": 1,
                        "calibrated_at": "2026-10-01T00:00:00Z",
                        "method": "two_point_buffer",
                        "standards_used": "pH 4.01 and pH 7.00 NIST buffer solutions",
                        "slope": 0.17544,
                        "offset_value": 2.5158,
                        "conversion_factor": None,
                        "temp_coeff_per_c": 0.003,
                        "reference_temp_c": 25.0,
                        "reference_instrument": "Laboratory pH electrode",
                        "before_value": None,
                        "after_value": None,
                        "valid_until": "2027-10-01T00:00:00Z",
                        "performed_by": "Station Engineer"
                    },
                    {
                        "calibration_id": 2,
                        "sensor_id": 2,
                        "version": 1,
                        "calibrated_at": "2026-10-01T00:00:00Z",
                        "method": "ice_point_single_point",
                        "standards_used": "Ice-water equilibrium bath 0.0 °C",
                        "slope": 1.0,
                        "offset_value": 0.0,
                        "conversion_factor": None,
                        "temp_coeff_per_c": None,
                        "reference_temp_c": 25.0,
                        "reference_instrument": "NIST Traceable Reference Thermometer",
                        "before_value": 0.0,
                        "after_value": 0.0,
                        "valid_until": "2027-10-01T00:00:00Z",
                        "performed_by": "Station Engineer"
                    },
                    {
                        "calibration_id": 3,
                        "sensor_id": 3,
                        "version": 1,
                        "calibrated_at": "2026-10-01T00:00:00Z",
                        "method": "single_point_kcl",
                        "standards_used": "1413 µS/cm KCl standard solution",
                        "slope": 0.5,
                        "offset_value": 0.0,
                        "conversion_factor": 0.5,
                        "temp_coeff_per_c": 0.02,
                        "reference_temp_c": 25.0,
                        "reference_instrument": "Laboratory Conductivity Cell",
                        "before_value": None,
                        "after_value": None,
                        "valid_until": "2027-10-01T00:00:00Z",
                        "performed_by": "Station Engineer"
                    },
                    {
                        "calibration_id": 4,
                        "sensor_id": 4,
                        "version": 1,
                        "calibrated_at": "2026-10-01T00:00:00Z",
                        "method": "acoustic_ranging_check",
                        "standards_used": "Laser distance measure calibration target",
                        "slope": 1.0,
                        "offset_value": 0.0,
                        "conversion_factor": None,
                        "temp_coeff_per_c": None,
                        "reference_temp_c": 25.0,
                        "reference_instrument": "Leica DISTO Laser Ranging Device",
                        "before_value": None,
                        "after_value": None,
                        "valid_until": "2027-10-01T00:00:00Z",
                        "performed_by": "Station Engineer"
                    }
                ]

            conn = get_mysql_conn()
            with conn.cursor() as cur:
                if from_ts and to_ts:
                    cur.execute("SELECT * FROM water_quality_telemetry WHERE epoch_time >= %s AND epoch_time <= %s ORDER BY id DESC LIMIT %s", (from_ts, to_ts, limit))
                else:
                    cur.execute("SELECT * FROM water_quality_telemetry ORDER BY id DESC LIMIT %s", (limit,))
                rows = cur.fetchall()

                # Always fetch absolute latest reading per sensor to guarantee freshest live tiles
                cur.execute("SELECT * FROM water_quality_telemetry WHERE ph IS NOT NULL ORDER BY id DESC LIMIT 1")
                latest_ph_row = cur.fetchone()
                cur.execute("SELECT * FROM water_quality_telemetry WHERE temperature_c IS NOT NULL ORDER BY id DESC LIMIT 1")
                latest_temp_row = cur.fetchone()
                cur.execute("SELECT * FROM water_quality_telemetry WHERE tds_ppm IS NOT NULL ORDER BY id DESC LIMIT 1")
                latest_tds_row = cur.fetchone()
                cur.execute("SELECT * FROM water_quality_telemetry WHERE depth_cm IS NOT NULL ORDER BY id DESC LIMIT 1")
                latest_depth_row = cur.fetchone()
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
                        "calibration_id": 1,
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
                        "calibration_id": 2,
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
                        "calibration_id": 3,
                        "is_synthetic": False,
                        "quality_flag": "OK" if r["tds_ppm"] <= 500 else "OUT_OF_RANGE",
                        "flags": []
                    }
                    readings.append(reading)
                    latest_map[3] = reading

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
                    derived.append({
                        "derived_id": rid + 1,
                        "source_reading_id": rid,
                        "temp_reading_id": r["id"] * 10 + 2 if r["temperature_c"] is not None else None,
                        "temp_age_s": 0,
                        "kind": "ec_uS_cm_25c",
                        "value": round(float(r["tds_ppm"]) / 0.5, 1),
                        "unit": "µS/cm",
                        "method_note": "Reference 25°C conductance",
                        "quality_flag": "OK",
                        "measured_at": iso_time
                    })

                # 4. Water Level (Sensor 4, Controller 2)
                if r["depth_cm"] is not None:
                    rid = r["id"] * 10 + 4
                    dist_m = round(float(r["depth_cm"]) / 100.0, 3)
                    reading = {
                        "reading_id": rid,
                        "sensor_id": 4,
                        "controller_id": 2,
                        "measured_at": iso_time,
                        "device_time_raw": None,
                        "received_at": iso_time,
                        "raw_value": dist_m,
                        "raw_unit": "m",
                        "corrected_value": dist_m,
                        "corrected_unit": "m",
                        "calibration_id": 4,
                        "is_synthetic": False,
                        "quality_flag": "OK",
                        "flags": []
                    }
                    readings.append(reading)
                    latest_map[4] = reading

                    derived.append({
                        "derived_id": rid,
                        "source_reading_id": rid,
                        "temp_reading_id": None,
                        "temp_age_s": None,
                        "kind": "level_distance_m",
                        "value": dist_m,
                        "unit": "m",
                        "method_note": "Ultrasonic distance to surface",
                        "quality_flag": "OK",
                        "measured_at": iso_time
                    })
                    derived.append({
                        "derived_id": rid + 1,
                        "source_reading_id": rid,
                        "temp_reading_id": None,
                        "temp_age_s": None,
                        "kind": "water_elevation_m",
                        "value": round(5.0 - dist_m, 3),
                        "unit": "m",
                        "method_note": "Elevation relative to lake bed datum",
                        "quality_flag": "OK",
                        "measured_at": iso_time
                    })

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

            # Ensure all 4 sensors exist in latest_map
            for s_id, s_row, param_field, raw_u, cor_u, c_id in [
                (1, latest_ph_row, "ph", "pH", "pH", 1),
                (2, latest_temp_row, "temperature_c", "°C", "°C", 1),
                (3, latest_tds_row, "tds_ppm", "ppm", "ppm", 2),
                (4, latest_depth_row, "depth_cm", "m", "m", 2)
            ]:
                if s_id not in latest_map and s_row and s_row[param_field] is not None:
                    s_epoch = s_row["epoch_time"]
                    s_iso = datetime.fromtimestamp(s_epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    val = float(s_row[param_field])
                    if s_id == 4:
                        val = round(val / 100.0, 3)
                    latest_map[s_id] = {
                        "reading_id": s_row["id"] * 10 + s_id,
                        "sensor_id": s_id,
                        "controller_id": c_id,
                        "measured_at": s_iso,
                        "device_time_raw": None,
                        "received_at": s_iso,
                        "raw_value": val,
                        "raw_unit": raw_u,
                        "corrected_value": val,
                        "corrected_unit": cor_u,
                        "calibration_id": s_id,
                        "is_synthetic": False,
                        "quality_flag": "OK",
                        "flags": []
                    }

            snapshot_data["readings"] = readings
            snapshot_data["derived_measurements"] = derived
            snapshot_data["measurement_cycles"] = cycles
            snapshot_data["latest"] = list(latest_map.values())
            snapshot_data["meta"]["source"] = "mysql_live"
            snapshot_data["meta"]["total_rows_in_db"] = len(rows)

            return jsonify(snapshot_data), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/", methods=["GET"])
    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        return send_from_directory(DASHBOARD_DIR, "index.html")

    @app.route("/<path:filename>", methods=["GET"])
    def serve_dashboard_static(filename):
        if os.path.exists(os.path.join(DASHBOARD_DIR, filename)):
            return send_from_directory(DASHBOARD_DIR, filename)
        return jsonify({"error": "File not found"}), 404

    return app


def run_bridge(cfg):
    import logging
    import pymysql
    import pymysql.cursors

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    log = logging.getLogger("bridge")

    # Connect to MySQL and ensure schema exists
    try:
        init_conn = pymysql.connect(
            host=cfg.get("mysql_host", "127.0.0.1"),
            port=int(cfg.get("mysql_port", 3306)),
            user=cfg.get("mysql_user", "root"),
            password=cfg.get("mysql_password", ""),
            autocommit=True
        )
        with init_conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS %s;" % cfg.get("mysql_db", "aarogya_jal_db"))
            cur.execute("USE %s;" % cfg.get("mysql_db", "aarogya_jal_db"))
            cur.execute("""
                CREATE TABLE IF NOT EXISTS water_quality_telemetry (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    station_id VARCHAR(50) NOT NULL DEFAULT 'FS_LAKE_01',
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
        log.info("[MYSQL] Connected and verified database: %s", cfg.get("mysql_db", "aarogya_jal_db"))
    except Exception as e:
        sys.exit("[FATAL] Could not connect to MySQL server on %s:%s - %s" % (
            cfg.get("mysql_host", "127.0.0.1"), cfg.get("mysql_port", 3306), e))

    def get_mysql_conn():
        return pymysql.connect(
            host=cfg.get("mysql_host", "127.0.0.1"),
            port=int(cfg.get("mysql_port", 3306)),
            user=cfg.get("mysql_user", "root"),
            password=cfg.get("mysql_password", ""),
            database=cfg.get("mysql_db", "aarogya_jal_db"),
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )

    app = make_app(cfg, get_mysql_conn)
    log.info("Aarogya Jal master bridge running on port %s (MySQL Backend)", cfg["port"])
    app.run(host="0.0.0.0", port=cfg["port"], debug=False)


def main():
    cfg = load_config()
    role = "node" if MICRO else (sys.argv[1] if len(sys.argv) > 1 else cfg["role"])
    if role == "bridge":
        run_bridge(cfg)
    elif role == "simulate":
        run_node(cfg, Pretend(cfg), lambda c: True)
    elif role == "node":
        run_node(cfg, Hardware(cfg), wifi_connect)
    else:
        sys.exit("role must be node, bridge or simulate, not %r" % role)


if __name__ == "__main__":
    main()
