#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include <Adafruit_BMP280.h>
#include <MQ135.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

const char* serverName = "your_domen";

const char* deviceId = "your_device_id";

#define SDA_PIN D2
#define SCL_PIN D1
#define MQ135PIN A0

Adafruit_AHTX0 aht;
Adafruit_BMP280 bmp;
MQ135 mq135(MQ135PIN);

float rzero = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(SDA_PIN, SCL_PIN);
  
  aht.begin();
  bmp.begin(0x76);
  
  delay(10000); 
  
  rzero = mq135.getRZero(); 

  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  delay(2000);
}

float readTemperature() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  float t=temp.temperature;

  if (isnan(t)) {
    return -1000;
  }

  return t;
}

float readHumidity() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  float h=humidity.relative_humidity;

  if (isnan(h)) {
    return -1000;
  }
  return h;
}

float readPressure() {
  float p=bmp.readPressure();
  if (isnan(p)) {
    return -1000;
  }
  return p/133.322;
}

float readCO2() {
  float ppm=mq135.getPPM();
  if (isnan(ppm)) {
    return -1000;
  }
  return ppm;
}

void sendData() {
  if (WiFi.status() != WL_CONNECTED) {
    return;
  }
  
  float temp = readTemperature();
  float humidity = readHumidity();
  float pressure = readPressure();
  float co2ppm = readCO2();

  std::unique_ptr<BearSSL::WiFiClientSecure> client(new BearSSL::WiFiClientSecure);
  client->setInsecure();  
  client->setTimeout(15000);  
  
  HTTPClient http;
  String url = String(serverName);

  if (!http.begin(*client, url)) {
    return;
  }
  
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(15000);

  StaticJsonDocument<300> doc;
  doc["temperature"] = temp;
  doc["humidity"] = humidity; 
  doc["pressure"] = pressure;
  doc["co2"] = co2ppm;
  doc["device_id"] = deviceId;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpCode = -1;
  int retries = 2;
  
  for (int i = 0; i < retries; i++) {
    httpCode = http.POST(jsonString);
    if (httpCode > 0) break;  
  }

  http.end();
}

void loop() {
  static unsigned long lastSend = 0;
  const unsigned long sendInterval = 10000;
  
  if (millis() - lastSend >= sendInterval) {
    sendData();
    lastSend = millis();
  }
  
  delay(1000);
}