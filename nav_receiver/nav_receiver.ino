// LORA Receiver
#include <ros.h>
#include <std_msgs/String.h>
#include <ArduinoJson.h>
#include <px4_controller/key.h>
#include <LoRa.h>
#include <SPI.h>
#include <string>

ros::NodeHandle nh;
std_msgs::String message;
px4_controller::key msg; // global variable
ros::Publisher chatter("/lora_messages", &message);

void setup() {
  nh.initNode();
  nh.advertise(chatter);
//   Serial.begin(9600);
//   while (!Serial);
//   Serial.println("LoRa Receiver");
  if (!LoRa.begin(915E6)) {
//     Serial.println("Starting LoRa failed!");
    while (1);
  }
}

String output;
void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  char c;
  nh.spinOnce();
  if (packetSize) {
    // read packet
    while (LoRa.available()) {
      c = (char)LoRa.read();
      if (c == 'u')
      {
        //  Publish the string and reset output
        message.data = output.c_str();
        chatter.publish( &message );
        //  Serial.println(output);
        output = "";
      }
      else
        output += String(c);
    }
  }
}
