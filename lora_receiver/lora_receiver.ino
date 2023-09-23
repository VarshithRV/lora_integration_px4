// LORA Receiver

#include <ArduinoJson.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <px4_controller/key.h>
#include <std_msgs/Empty.h>
#include <LoRa.h>
#include <SPI.h>


void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Receiver");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
  }
}
