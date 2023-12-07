//code written by Dillon Geary for CSC 49008 final

#include<ESP8266WiFi.h>
const char *ssid = "LU-Robotics";
const char *password ="r2d2c3po";
const char *dweetsite = "dweet.io";
void connectToWiFi() {
//Connect to WiFi Network
   Serial.println();
   Serial.println();
   Serial.print("Connecting to WiFi");
   Serial.println("...");
   WiFi.begin(ssid, password);
   int retries = 0;
while ((WiFi.status() != WL_CONNECTED) && (retries < 15)) {
   retries++;
   delay(500);
   Serial.print(".");
}
if (retries > 14) {
    Serial.println(F("WiFi connection FAILED"));
}
if (WiFi.status() == WL_CONNECTED) {
    Serial.println(F("WiFi connected!"));
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
    Serial.println(F("Setup ready"));
}
// connect to dweet and send the dweet
void dweetMake(int val){
    WiFiClient client;
    const int httpPort = 80;
    if(!client.connect(dweetsite,httpPort)){
      Serial.println("Connection Failed");
      return;
    }
    String dweetstring="GET /dweet/for/DGPS1?Status="+String(val);
    dweetstring=dweetstring + " HTTP/1.1\r\n"+
    "Host: " + dweetsite + "\r\n + Connection: close\r\n\r\n";
    client.print(dweetstring);
    delay(10);
    while(client.available()){
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }
    return ;
}
//set pins and run serial for debugging
void setup() {
  Serial.begin(9600);
  delay(100);
  connectToWiFi();
  pinMode(D0,OUTPUT);
  pinMode(D1,OUTPUT);
}

void loop() {
  int value = analogRead(A0);
  if(value<700){ //if a car is on the sensor
    //change light to red
    digitalWrite(D0,HIGH);
    digitalWrite(D1,LOW);
    //small delay to make sure the dweet gets sent as without it it was running into problems
    delay(100);
    dweetMake(0);
    while(value<700){//wait for it to change
      delay(100);
      value = analogRead(A0);
    }
  }
  //opposite of above
  else if(value>700){
    digitalWrite(D0,LOW);
    digitalWrite(D1,HIGH);
    delay(100);
    dweetMake(1);
    while(value>700){
      //Serial.println(String(value));
      delay(100);
      value = analogRead(A0);
    }
  } 
  }

