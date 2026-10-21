/*
 * ==============================================================================
 * AAROGYA JAL - UNIFIED 4-SENSOR NODE (ESP8266 NODEMCU)
 * Reads all 4 water quality parameters and transmits to SQL Database Bridge:
 *   1. pH Level (Analog A0 via D1 Power Switch)
 *   2. TDS Level (Analog A0 via D5 Power Switch)
 *   3. Water Temperature (DS18B20 1-Wire on Pin D2)
 *   4. Lake Depth / Clearance (HC-SR04 Ultrasonic on D7 Trig / D6 Echo)
 * ==============================================================================
 * WIRING GUIDE FOR SINGLE ESP8266:
 * - DS18B20 Temp Data:    D2 (GPIO 4) with 4.7k pullup resistor to 3.3V
 * - Ultrasonic TRIG:      D7 (GPIO 13)
 * - Ultrasonic ECHO:      D6 (GPIO 12)
 * - Shared Analog A0:     Connected to BOTH pH & TDS Analog Signal Pins
 * - pH Module VCC:        D1 (GPIO 5) [Software Power Switched]
 * - TDS Module VCC:       D5 (GPIO 14) [Software Power Switched]
 * - All GNDs:             Common ESP8266 GND
 * Note: Power switching prevents electrical cross-talk in water and allows
 *       two analog sensors to share the single ESP8266 A0 pin seamlessly!
 * ==============================================================================
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- 1. WiFi & Server Configuration ---
const char *ssid = "OnePlus 9R";          // WiFi SSID
const char *pass = "zxcvbnmz";            // WiFi Password

// Update this with your Laptop's current IP address
// Example: http://10.100.205.12:5000/api/telemetry
const char* serverUrl = "http://10.100.205.12:5000/api/telemetry";
const char* stationId = "FS_LAKE_STATION_01";
const char* lakeName  = "Fateh Sagar Lake";

// --- 2. Pin Definitions ---
#define SENSOR_ADC_PIN  A0     // Shared Analog Pin
#define PH_POWER_PIN    D1     // GPIO 5 - Controls VCC of pH Module
#define TDS_POWER_PIN   D5     // GPIO 14 - Controls VCC of TDS Module

#define ONE_WIRE_BUS    D2     // GPIO 4 - DS18B20 Temperature Data
#define TRIG_PIN        D7     // GPIO 13 - Ultrasonic Trigger
#define ECHO_PIN        D6     // GPIO 12 - Ultrasonic Echo

// --- 3. Sensor Objects & Variables ---
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensors(&oneWire);

// Calibration constants
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
  Serial.println("  AAROGYA JAL - UNIFIED 4-SENSOR WATER NODE (ESP8266)   ");
  Serial.println("========================================================");

  // Configure pins
  pinMode(PH_POWER_PIN, OUTPUT);
  pinMode(TDS_POWER_PIN, OUTPUT);
  digitalWrite(PH_POWER_PIN, LOW);
  digitalWrite(TDS_POWER_PIN, LOW);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT_PULLUP);

  // Initialize Temperature sensor
  tempSensors.begin();
  Serial.println("[SETUP] DS18B20 Temperature sensor initialized.");

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  Serial.print("[WIFI] Connecting to SSID: ");
  Serial.println(ssid);

  int wifiAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && wifiAttempts < 30) {
    delay(500);
    Serial.print(".");
    wifiAttempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WIFI] Connected successfully!");
    Serial.print("[WIFI] Node IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WIFI] Connection timeout - continuing in offline loop mode...");
  }
}

void loop() {
  Serial.println("\n----------------- [SAMPLING SENSORS] -----------------");

  // 1. Read Water Temperature (Needed first for TDS temperature compensation)
  float water_temp = readWaterTemperature();
  Serial.print("1. Water Temperature: ");
  Serial.print(water_temp, 2);
  Serial.println(" °C");

  // 2. Read pH Value (Switches ON D1, reads A0, switches OFF D1)
  float ph_val = readPHValue();
  Serial.print("2. pH Level:          ");
  Serial.println(ph_val, 2);

  // 3. Read TDS Value (Switches ON D5, reads A0, switches OFF D5)
  float tds_val = readTDSValue(water_temp);
  Serial.print("3. TDS Level:         ");
  Serial.print(tds_val, 1);
  Serial.println(" ppm");

  // 4. Read Depth / Distance
  float depth_cm = readWaterDepth();
  Serial.print("4. Water Clearance:   ");
  Serial.print(depth_cm, 1);
  Serial.println(" cm");

  // 5. Transmit all 4 readings to SQL Bridge Server via HTTP POST
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    Serial.println("\n[HTTP] Sending unified 4-sensor payload to SQL database...");

    if (http.begin(client, serverUrl)) {
      http.addHeader("Content-Type", "application/json");

      // Construct JSON payload
      String jsonPayload = "{";
      jsonPayload += "\"station_id\":\"" + String(stationId) + "\",";
      jsonPayload += "\"lakename\":\"" + String(lakeName) + "\",";
      jsonPayload += "\"ph\":" + String(ph_val, 2) + ",";
      jsonPayload += "\"tds\":" + String(tds_val, 1) + ",";
      jsonPayload += "\"temperature\":" + String(water_temp, 2) + ",";
      jsonPayload += "\"depth\":" + String(depth_cm, 1) + ",";
      jsonPayload += "\"source_device\":\"ESP8266_UNIFIED_NODE\"";
      jsonPayload += "}";

      int httpResponseCode = http.POST(jsonPayload);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.printf("[HTTP SUCCESS] Code %d -> Response: %s\n", httpResponseCode, response.c_str());
      } else {
        Serial.printf("[HTTP ERROR] Failed POST request, code: %d, err: %s\n", 
                      httpResponseCode, http.errorToString(httpResponseCode).c_str());
      }
      http.end();
    } else {
      Serial.println("[HTTP ERROR] Unable to initiate connection to serverUrl");
    }
  } else {
    Serial.println("[WIFI] WiFi disconnected, attempting reconnect...");
    WiFi.reconnect();
  }

  // Sample every 5 seconds
  Serial.println("[LOOP] Sleeping 5 seconds before next reading...");
  delay(5000);
}

// ==============================================================================
// SENSOR READING IMPLEMENTATIONS
// ==============================================================================

float readWaterTemperature() {
  tempSensors.requestTemperatures();
  float t = tempSensors.getTempCByIndex(0);
  if (t < -50.0 || t > 85.0) {
    return 24.5; // Fallback baseline if sensor disconnected
  }
  return t;
}

float readPHValue() {
  // Power ON pH sensor module
  digitalWrite(PH_POWER_PIN, HIGH);
  digitalWrite(TDS_POWER_PIN, LOW);
  delay(100); // Allow sensor voltage to settle

  int samples[10];
  for (int i = 0; i < 10; i++) {
    samples[i] = analogRead(SENSOR_ADC_PIN);
    delay(20);
  }

  // Turn OFF pH sensor module to prevent interference
  digitalWrite(PH_POWER_PIN, LOW);

  // Bubble sort for median filter
  for (int i = 0; i < 9; i++) {
    for (int j = i + 1; j < 10; j++) {
      if (samples[i] > samples[j]) {
        int temp = samples[i];
        samples[i] = samples[j];
        samples[j] = temp;
      }
    }
  }

  // Average middle 6 readings
  long avgRaw = 0;
  for (int i = 2; i < 8; i++) {
    avgRaw += samples[i];
  }
  float volt = (float)avgRaw * 3.3 / 1024.0 / 6.0;
  float ph = -5.70 * volt + ph_calibration_value;

  if (ph < 0.0) ph = 0.0;
  if (ph > 14.0) ph = 14.0;
  return ph;
}

float readTDSValue(float currentTemp) {
  // Power ON TDS sensor module
  digitalWrite(TDS_POWER_PIN, HIGH);
  digitalWrite(PH_POWER_PIN, LOW);
  delay(100); // Allow sensor excitation voltage to settle

  int samples[TDS_SAMPLES];
  for (int i = 0; i < TDS_SAMPLES; i++) {
    samples[i] = analogRead(SENSOR_ADC_PIN);
    delay(15);
  }

  // Turn OFF TDS sensor module
  digitalWrite(TDS_POWER_PIN, LOW);

  // Bubble sort for median extraction
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
  float averageVoltage = (float)medianRaw * (float)VREF / 1024.0;

  // Temperature compensation formula
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

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout (~5 meters)
  if (duration == 0) {
    return 0.0; // Out of range or no echo
  }

  float distance_cm = (duration * 0.0343) / 2.0;
  return distance_cm;
}
