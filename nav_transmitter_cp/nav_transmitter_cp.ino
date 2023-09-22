/*
LORA Transmitter from the ground station, subscribes to the /keyboard from the teleop node
*/

#include <ArduinoJson.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <px4_controller/key.h>
#include <std_msgs/Empty.h>
#include <LoRa.h>
#include <SPI.h>

ros::NodeHandle nh;
px4_controller::key keypress;
StaticJsonDocument<100> doc;
String json_string;

// demo publisher
std_msgs::String str_msg;
ros::Publisher chatter("/chatter", &str_msg);

void messageCb( const px4_controller::key& msg){
  doc["w"] = msg.w;
  doc["a"] = msg.a;
  doc["s"] = msg.s;
  doc["d"] = msg.d;
  doc["q"] = msg.q;
  doc["e"] = msg.e;
  doc["z"] = msg.z;
  doc["x"] = msg.x;
  doc["c"] = msg.c;
  doc["lshift"] = msg.key_left_shift;
  doc["lctrl"] = msg.key_left_ctrl;
  doc["left"] = msg.key_left;
  doc["right"] = msg.key_right;
  serializeJson(doc,json_string);
  str_msg.data = json_string.c_str();
  chatter.publish( &str_msg );
}

ros::Subscriber<px4_controller::key> sub("/keyboard", messageCb );
void setup()
{
  Serial.begin(9600);
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub);
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop()
{
  // transmit the json string through lora here.
  while(1){
//    LoRa.beginPacket();
//    LoRa.print(json_string);
//    LoRa.endPacket();
//    str_msg.data = ::json_string.c_str();
//    chatter.publish( &str_msg );
    nh.spinOnce();
    delay(500); 
  }
}
