#include "ESP8266WiFi.h"
#include "WiFiClient.h"

//===============================================
// WiFi config
//===============================================
const char* apName = "your_ap_name";
const char* apPassword = "your_ap_password";
IPAddress staticIP(192,168,128,1);
IPAddress gateway(192,168,128,1);
IPAddress subnet(255,255,255,0);

//===============================================
// Server
//===============================================
WiFiServer server(80);

//===============================================
// Setup
//===============================================
void setup() {
  Serial.begin(115200);
  Serial.println();

  WiFi.mode(WIFI_AP);

  Serial.print("Setting soft-AP configuration ... ");
  Serial.println(WiFi.softAPConfig(staticIP, gateway, subnet) ? "Ready" : "Failed!");

  Serial.print("Setting soft-AP ... ");
  Serial.println(WiFi.softAP(apName, apPassword) ? "Ready" : "Failed!");

  Serial.print("Soft-AP IP address = ");
  Serial.println(WiFi.softAPIP());

  Serial.printf("Stations connected to soft-AP = %d\n", WiFi.softAPgetStationNum());

  // Initialize server
  server.begin();
}

//===============================================
// Loop
//===============================================
void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient client = server.available();
  if (!client){
    Serial.println("Wait for client...");
    delay(100);
    return ;
  }

  Serial.println("A new client is connected!");

  String data = "";
  while (client.connected()) {
    while (client.available()>0) {
      data += char(client.read());
    }
    if (data != ""){
      Serial.println(data);
      client.print("Hi! I am server~");
      data = "";
    }
    delay(10);
  }
  client.stop();
  Serial.println("Client disconnected");
}
