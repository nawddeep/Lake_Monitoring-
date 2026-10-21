/*
 * ==============================================================================
 * AAROGYA JAL - UNIFIED 4-SENSOR WATER NODE (ESP32 DUAL-CORE)
 * Reads all 4 water quality parameters and transmits to SQL Database Bridge:
 *   1. pH Level (Direct 12-bit ADC on GPIO 34)
 *   2. TDS Level (Direct 12-bit ADC on GPIO 35)
 *   3. Water Temperature (DS18B20 1-Wire on GPIO 4)
 *   4. Lake Depth / Clearance (HC-SR04 Ultrasonic on GPIO 5 Trig / GPIO 18 Echo)
 * ==============================================================================
 * ESP32 PINOUT ADVANTAGE:
 * ESP32 features multiple independent ADC channels, so pH and TDS do NOT require
 * any external multiplexer or power-switching!
 * ==============================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- 1. WiFi & Server Configuration ---
const char *ssid = "OnePlus 9R";          // WiFi SSID
const char *pass = "zxcvbnmz";            // WiFi Password

// Update with your Laptop's current IP address
const char* serverUrl = "http://10.100.205.12:5000/api/telemetry";
const char* stationId = "FS_LAKE_STATION_01";
const char* lakeName  = "Fateh Sagar Lake";

// --- 2. Pin Definitions ---
#define PH_PIN          34     // ADC1_CH6
#define TDS_PIN         35     // ADC1_CH7
#define ONE_WIRE_BUS    4      // DS18B20 1-Wire (with 4.7k pullup)
#define TRIG_PIN        5      // HC-SR04 Trigger
#define ECHO_PIN        18     // HC-SR04 Echo

// --- 3. Sensor Objects & Constants ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensors(&oneWire);

float ph_calibration_value = 21.34;
#define VREF 3.3
#define TDS_SAMPLES 20

// Function prototypes
float readWaterTemperature();
float readPHValue();
float readTDSValue(float currentTemp);
float readWaterDepth();

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n========================================================");
  Serial.println("    AAROGYA JAL - UNIFIED 4-SENSOR NODE (ESP32)         ");
  Serial.println("========================================================");

  // Configure pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Initialize Temperature sensor
  tempSensors.begin();
  Serial.println("[SETUP] DS18B20 Temperature sensor ready.");

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  Serial.print("[WIFI] Connecting to ");
  Serial.println(ssid);

  int wifiAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && wifiAttempts < 30) {
    delay(500);
    Serial.print(".");
    wifiAttempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI] Connected! Node IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WIFI] Connection timeout - continuing in offline loop mode...");
  }
}

void loop() {
  Serial.println("\n----------------- [SAMPLING SENSORS] -----------------");

  // 1. Water Temperature
  float water_temp = readWaterTemperature();
  Serial.print("1. Water Temperature: ");
  Serial.print(water_temp, 2);
  Serial.println(" °C");

  // 2. pH Level
  float ph_val = readPHValue();
  Serial.print("2. pH Level:          ");
  Serial.println(ph_val, 2);

  // 3. TDS Level
  float tds_val = readTDSValue(water_temp);
  Serial.print("3. TDS Level:         ");
  Serial.print(tds_val, 1);
  Serial.println(" ppm");

  // 4. Lake Clearance / Depth
  float depth_cm = readWaterDepth();
  Serial.print("4. Water Clearance:   ");
  Serial.print(depth_cm, 1);
  Serial.println(" cm");

  // 5. Transmit all 4 readings to SQL Bridge Server via HTTP POST
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    Serial.println("\n[HTTP] Sending unified 4-sensor payload to SQL database...");

    if (http.begin(serverUrl)) {
      http.addHeader("Content-Type", "application/json");

      String jsonPayload = "{";
      jsonPayload += "\"station_id\":\"" + String(stationId) + "\",";
      jsonPayload += "\"lakename\":\"" + String(lakeName) + "\",";
      jsonPayload += "\"ph\":" + String(ph_val, 2) + ",";
      jsonPayload += "\"tds\":" + String(tds_val, 1) + ",";
      jsonPayload += "\"temperature\":" + String(water_temp, 2) + ",";
      jsonPayload += "\"depth\":" + String(depth_cm, 1) + ",";
      jsonPayload += "\"source_device\":\"ESP32_UNIFIED_NODE\"";
      jsonPayload += "}";

      int httpResponseCode = http.POST(jsonPayload);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.printf("[HTTP SUCCESS] Code %d -> Response: %s\n", httpResponseCode, response.c_str());
      } else {
        Serial.printf("[HTTP ERROR] POST failed, code: %d, err: %s\n", 
                      httpResponseCode, http.errorToString(httpResponseCode).c_str());
      }
      http.end();
    }
  } else {
    Serial.println("[WIFI] Disconnected, reconnecting...");
    WiFi.reconnect();
  }

  delay(5000);
}

float readWaterTemperature() {
  tempSensors.requestTemperatures();
  float t = tempSensors.getTempCByIndex(0);
  if (t < -50.0 || t > 85.0) return 24.5;
  return t;
}

float readPHValue() {
  int samples[10];
  for (int i = 0; i < 10; i++) {
    samples[i] = analogRead(PH_PIN);
    delay(20);
  }

  // Sort samples
  for (int i = 0; i < 9; i++) {
    for (int j = i + 1; j < 10; j++) {
      if (samples[i] > samples[j]) {
        int temp = samples[i];
        samples[i] = samples[j];
        samples[j] = temp;
      }
    }
  }

  // Average middle 6
  long avgRaw = 0;
  for (int i = 2; i < 8; i++) avgRaw += samples[i];
  
  // ESP32 ADC is 12-bit (0-4095)
  float volt = (float)avgRaw * 3.3 / 4095.0 / 6.0;
  float ph = -5.70 * volt + ph_calibration_value;
  if (ph < 0.0) ph = 0.0;
  if (ph > 14.0) ph = 14.0;
  return ph;
}

float readTDSValue(float currentTemp) {
  int samples[TDS_SAMPLES];
  for (int i = 0; i < TDS_SAMPLES; i++) {
    samples[i] = analogRead(TDS_PIN);
    delay(15);
  }

  for (int i = 0; i < TDS_SAMPLES - 1; i++) {
    for (int j = i + 1; j < TDS_SAMPLES; j++) {
      if (samples[i] > samples[j]) {
        int temp = samples[i];
        samples[i] = samples[j];
        samples[j] = temp;
      }
    }
  }

  int medianRaw = samples[TDS_SAMPLES / 2];
  float averageVoltage = (float)medianRaw * (float)VREF / 4095.0;

  float compensationCoefficient = 1.0 + 0.02 * (currentTemp - 25.0);
  float compensationVoltage = averageVoltage / compensationCoefficient;

  float tds = (133.42 * compensationVoltage * compensationVoltage * compensationVoltage 
              - 255.86 * compensationVoltage * compensationVoltage 
              + 857.39 * compensationVoltage) * 0.5;

  if (tds < 0.0) tds = 0.0;
  return tds;
}

float readWaterDepth() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return 0.0;
  return (duration * 0.0343) / 2.0;
}
