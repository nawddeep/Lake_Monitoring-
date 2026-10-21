# ESP MicroPython Client Node for Aarogya Jal
import time
import json
import sys
import machine

# MicroPython Epoch
EPOCH_OFFSET = 946684800 if time.gmtime(0)[0] == 2000 else 0

CONFIG = {
    "station_id": "FS_LAKE_01",
    "node_id": "esp_node",
    "lake_name": "Fateh Sagar Lake",
    "wifi_ssid": "OnePlus 9R",
    "wifi_password": "zxcvbnmz",
    "bridge_host": "10.59.168.155",
    "bridge_port": 5000,
    "bridge_path": "/api/telemetry",
    "sample_s": 5,
    "post_s": 5,
    "adc_full_scale_v": 3.3,
    "ph7_voltage": 2.5158,
    "volts_per_ph": 0.17544,
    # Pins
    "temp_pin": 4,      # D2 on ESP8266
    "trig_pin": 13,     # D7
    "echo_pin": 12,     # D6
}

def sleep_ms(ms):
    time.sleep_ms(ms)

def wifi_connect(ssid, password, max_wait=20):
    import network
    w = network.WLAN(network.STA_IF)
    w.active(True)
    if not w.isconnected():
        print("[WIFI] Connecting to", ssid)
        w.connect(ssid, password)
        start = time.time()
        while not w.isconnected() and time.time() - start < max_wait:
            time.sleep_ms(500)
            print(".", end="")
        print()
    if w.isconnected():
        print("[WIFI] Connected! IP:", w.ifconfig()[0])
        try:
            import ntptime
            ntptime.settime()
        except:
            pass
        return True
    print("[WIFI] Connection failed")
    return False

class Sensors:
    def __init__(self):
        # ADC
        self.adc = machine.ADC(0)
        # DS18B20 Temp
        self.roms = []
        try:
            import ds18x20, onewire
            self.ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(CONFIG["temp_pin"])))
            self.roms = self.ds.scan()
            print("[SENSORS] DS18B20 found:", self.roms)
        except Exception as e:
            print("[SENSORS] DS18B20 init note:", e)
        # Ultrasonic
        try:
            self.trig = machine.Pin(CONFIG["trig_pin"], machine.Pin.OUT)
            self.echo = machine.Pin(CONFIG["echo_pin"], machine.Pin.IN)
        except Exception as e:
            print("[SENSORS] Ultrasonic init note:", e)

    def read_adc_volts(self, samples=10):
        raw = []
        for _ in range(samples):
            raw.append(self.adc.read())
            time.sleep_ms(15)
        raw.sort()
        # Average middle samples
        mid = raw[2:-2] if len(raw) >= 6 else raw
        avg_raw = sum(mid) / len(mid)
        # ESP8266 ADC0 is 10-bit (0-1023)
        return (avg_raw / 1023.0) * CONFIG["adc_full_scale_v"]

    def read_temperature(self):
        if not self.roms:
            return 26.5 # Reasonable fallback when disconnected
        try:
            self.ds.convert_temp()
            time.sleep_ms(750)
            t = self.ds.read_temp(self.roms[0])
            if -5.0 < t < 70.0 and t != 85.0:
                return round(t, 2)
        except:
            pass
        return 26.5

    def read_distance_cm(self):
        try:
            self.trig.value(0)
            time.sleep_us(2)
            self.trig.value(1)
            time.sleep_us(15)
            self.trig.value(0)
            us = machine.time_pulse_us(self.echo, 1, 30000)
            if us > 0:
                dist = us / 58.0
                if 20.0 <= dist <= 500.0:
                    return round(dist, 1)
        except:
            pass
        return 45.0 # Simulated baseline lake clearance if unattached

def http_post(host, port, path, payload_dict):
    try:
        import usocket as socket
    except:
        import socket

    data = json.dumps(payload_dict).encode('utf-8')
    header = (
        "POST %s HTTP/1.0\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n"
    ) % (path, host, len(data))

    s = socket.socket()
    try:
        s.settimeout(6)
        addr = socket.getaddrinfo(host, port)[0][-1]
        s.connect(addr)
        s.sendall(header.encode('utf-8') + data)
        resp = s.recv(128)
        if not resp:
            print("[HTTP] Empty response received")
            return False
        status_line = resp.split(b"\r\n")[0].decode('utf-8', 'ignore')
        print("[HTTP] Server responded:", status_line)
        return ("200" in status_line) or ("201" in status_line)
    except Exception as e:
        print("[HTTP] Post exception:", e)
        return False
    finally:
        s.close()

def run():
    print("========================================")
    print("   Aarogya Jal MicroPython Node Start   ")
    print("========================================")
    
    wifi_connect(CONFIG["wifi_ssid"], CONFIG["wifi_password"])
    sensors = Sensors()

    seq = 0
    while True:
        try:
            temp_c = sensors.read_temperature()
            volts = sensors.read_adc_volts()
            dist_cm = sensors.read_distance_cm()

            # pH conversion
            ph_val = 7.0 + (CONFIG["ph7_voltage"] - volts) / (CONFIG["volts_per_ph"] * (273.15 + temp_c) / 298.15)
            ph_val = round(max(0.0, min(14.0, ph_val)), 2)

            # TDS conversion
            v_tds = volts / (1.0 + 0.02 * (temp_c - 25.0))
            tds_ppm = max(0.0, (133.42 * v_tds**3 - 255.86 * v_tds**2 + 857.39 * v_tds) * 0.5)
            tds_ppm = round(tds_ppm, 1)

            now_ts = int(time.time() + EPOCH_OFFSET)
            payload = {
                "station_id": CONFIG["station_id"],
                "lakename": CONFIG["lake_name"],
                "temperature": temp_c,
                "ph": ph_val,
                "tds": tds_ppm,
                "depth": dist_cm,
                "source_device": "ESP_MICROPYTHON_NODE"
            }

            print("[TELEMETRY #%d] Temp=%.2f C | pH=%.2f | TDS=%.1f ppm | Depth=%.1f cm" % 
                  (seq, temp_c, ph_val, tds_ppm, dist_cm))

            ok = http_post(CONFIG["bridge_host"], CONFIG["bridge_port"], CONFIG["bridge_path"], payload)
            if ok:
                print("  -> Sent successfully to Dashboard & MySQL!")
            else:
                print("  -> Transmission failed, reconnecting WiFi...")
                wifi_connect(CONFIG["wifi_ssid"], CONFIG["wifi_password"], max_wait=5)

        except Exception as err:
            print("[ERROR in loop]:", err)

        time.sleep(CONFIG["post_s"])

if __name__ == "__main__":
    run()
