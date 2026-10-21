/*
 * ==============================================================================
 * AAROGYA JAL - ESP8266 NODE MCU: pH & TEMPERATURE SENSOR NODE
 * Sends live sensor readings directly to MongoDB Ingestion Bridge
 * ==============================================================================
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// --- WiFi Credentials ---
const char *ssid = "OnePlus 9R";     // Your WiFi SSID
const char *pass = "zxcvbnmz";        // Your WiFi Password

// --- Target Ingestion Bridge Server ---
// Your laptop's current Wi-Fi IP: 10.100.205.12
const char* serverUrl = "http://10.100.205.12:5000/temp_ph.php";
const char* lakeName  = "Fateh%20Sagar%20Lake";

// --- DS18B20 Temperature Pin ---
#define ONE_WIRE_BUS D2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// --- pH Sensor Configuration ---
#define PH_PIN A0
float calibration_value = 21.34;
int buffer_arr[10], temp_sort;
unsigned long int avgval;

void setup() {
  Serial.begin(115200);
  Serial.println("\n[SETUP] Starting Aarogya Jal pH & Temp Node...");
  
  sensors.begin();
  delay(1000);

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  Serial.print("[WIFI] Connecting to ");
  Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[WIFI] Connected! IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // 1. Read pH Value with 10-sample analog smoothing
  for (int i = 0; i < 10; i++) {
    buffer_arr[i] = analogRead(PH_PIN);
    delay(30);
  }
  // Sort analog buffer (Median filter)
  for (int i = 0; i < 9; i++) {
    for (int j = i + 1; j < 10; j++) {
      if (buffer_arr[i] > buffer_arr[j]) {
        temp_sort = buffer_arr[i];
        buffer_arr[i] = buffer_arr[j];
        buffer_arr[j] = temp_sort;
      }
    }
  }
  // Average middle 6 samples
  avgval = 0;
  for (int i = 2; i < 8; i++) {
    avgval += buffer_arr[i];
  }
  float volt = (float)avgval * 3.3 / 1024.0 / 6.0;
  float ph_act = -5.70 * volt + calibration_value;

  // 2. Read DS18B20 Water Temperature
  sensors.requestTemperatures();
  float water_temp = sensors.getTempCByIndex(0);

  Serial.println("----------------------------------------");
  Serial.print("pH Value: "); Serial.println(ph_act);
  Serial.print("Water Temperature: "); Serial.print(water_temp); Serial.println(" C");

  // 3. Send Data to MongoDB Bridge Server via HTTP GET
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String requestUrl = String(serverUrl) + 
                        "?lakename=" + String(lakeName) + 
                        "&temperature=" + String(water_temp, 2) + 
                        "&phlevel=" + String(ph_act, 2);

    Serial.print("[HTTP] Sending to: ");
    Serial.println(requestUrl);

    if (http.begin(client, requestUrl)) {
      int httpCode = http.GET();
      if (httpCode > 0) {
        Serial.printf("[HTTP] GET Success, Code: %d\n", httpCode);
        String payload = http.getString();
        Serial.print("[SERVER RESPONSE] ");
        Serial.println(payload);
      } else {
        Serial.printf("[HTTP] GET Failed, Error: %s\n", http.errorToString(httpCode).c_str());
      }
      http.end();
    }
  } else {
    Serial.println("[WIFI] Disconnected! Reconnecting...");
    WiFi.reconnect();
  }

  // Sample every 15 seconds
  Serial.println("[SLEEP] Waiting 15 seconds...");
  delay(1000);
}
