#include "ESP8266WiFi.h"
#include "WiFiClient.h"
#include "ESP8266WebServer.h"

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
ESP8266WebServer server(80);

//===============================================
// Functions
//===============================================
// For checking whether this WiFi board has been assigned to a static ip address
void handleCheckConnection(){
  Serial.println("Connect Successfully");
  server.send(200, "text/html", "success");
}
// Test - How arduino gets the paremeters
void handleGetArgTest(){
  for (int i = 0 ; i < server.args() ; i++){
    Serial.print("Arg ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(server.arg(i));
  }
  server.send(200, "text/html", "success");
}
// Example - You can copy this function for implementation.
void handleExampleFunction(){
  server.send(200, "text/html", "Hello World!");
}

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

  // Initialize server functions
  server.on("/", handleCheckConnection);
  server.on("/GetArgTest", handleGetArgTest);
  server.on("/ExampleFunction", handleExampleFunction);
  //------- Add new function in this block -------//
  // Your function here
  
  //----------------------------------------------//
  server.begin();
}

//===============================================
// Loop
//===============================================
void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();
}
