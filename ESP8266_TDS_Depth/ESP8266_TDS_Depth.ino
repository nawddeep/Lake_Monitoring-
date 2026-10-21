/*
 * ==============================================================================
 * AAROGYA JAL - ESP8266 NODE MCU: TDS & WATER DEPTH SENSOR NODE
 * Sends live sensor readings directly to MongoDB Ingestion Bridge
 * ==============================================================================
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

// --- WiFi Credentials ---
const char *ssid = "OnePlus 9R";     // Your WiFi SSID
const char *pass = "zxcvbnmz";        // Your WiFi Password

// --- Target Ingestion Bridge Server ---
// Your laptop's current Wi-Fi IP: 10.100.205.12
const char* serverUrl = "http://10.100.205.12:5000/tds_depth.php";
const char* lakeName  = "Fateh%20Sagar%20Lake";

// --- Ultrasonic Pins ---
#define TRIG D7
#define ECHO D6

// --- TDS Sensor Configuration ---
#define TdsSensorPin A0
#define VREF 3.3
#define SCOUNT 30

int analogBuffer[SCOUNT];
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0;
int copyIndex = 0;
float averageVoltage = 0;
float tdsValue = 0;
float defaultTemp = 24.0; // Temperature compensation baseline

int getMedianNum(int bArray[], int iFilterLen) {
  int bTab[iFilterLen];
  for (byte i = 0; i < iFilterLen; i++) bTab[i] = bArray[i];
  int i, j, bTemp;
  for (j = 0; j < iFilterLen - 1; j++) {
    for (i = 0; i < iFilterLen - j - 1; i++) {
      if (bTab[i] > bTab[i + 1]) {
        bTemp = bTab[i];
        bTab[i] = bTab[i + 1];
        bTab[i + 1] = bTemp;
      }
    }
  }
  if ((iFilterLen & 1) > 0) return bTab[(iFilterLen - 1) / 2];
  else return (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
}

void setup() {
  Serial.begin(115200);
  Serial.println("\n[SETUP] Starting Aarogya Jal TDS & Depth Node...");

  pinMode(TdsSensorPin, INPUT);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT_PULLUP);

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
  // 1. Sample TDS Analog Buffer
  for (int i = 0; i < SCOUNT; i++) {
    analogBuffer[i] = analogRead(TdsSensorPin);
    delay(20);
  }

  for (copyIndex = 0; copyIndex < SCOUNT; copyIndex++) {
    analogBufferTemp[copyIndex] = analogBuffer[copyIndex];
  }

  averageVoltage = getMedianNum(analogBufferTemp, SCOUNT) * (float)VREF / 1024.0;
  float compensationCoefficient = 1.0 + 0.02 * (defaultTemp - 25.0);
  float compensationVoltage = averageVoltage / compensationCoefficient;

  tdsValue = (133.42 * compensationVoltage * compensationVoltage * compensationVoltage 
              - 255.86 * compensationVoltage * compensationVoltage 
              + 857.39 * compensationVoltage) * 0.5;

  if (tdsValue < 0) tdsValue = 0;

  // 2. Measure Ultrasonic Distance (Lake Depth / Water Clearance)
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(20);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 30000); // 30ms timeout
  float distance_cm = 0;
  if (duration > 0) {
    distance_cm = (float)duration / 58.0;
  }

  Serial.println("----------------------------------------");
  Serial.print("TDS Value: "); Serial.print(tdsValue, 1); Serial.println(" ppm");
  Serial.print("Distance/Depth: "); Serial.print(distance_cm, 1); Serial.println(" cm");

  // 3. Send Data to MongoDB Bridge Server via HTTP GET
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String requestUrl = String(serverUrl) + 
                        "?lakename=" + String(lakeName) + 
                        "&tds=" + String(tdsValue, 1) + 
                        "&depth=" + String(distance_cm, 1);

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
