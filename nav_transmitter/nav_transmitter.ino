// publishes string to chatter and subscribes to /keyboard input from the teleop key

#include <ros.h>
#include <std_msgs/String.h>
#include <ArduinoJson.h>
#include <px4_controller/key.h>
#include <LoRa.h>
#include <SPI.h>
#include <string>


using namespace std;

typedef struct bits
{
    unsigned x:1;
} bits;

ros::NodeHandle nh;
std_msgs::String str_msg;
px4_controller::key msg; // global variable

void messageCb( const px4_controller::key& received_msg){
  msg=received_msg; // update the global variable
}

// Publisher and subscribers
ros::Subscriber<px4_controller::key> sub("/keyboard", &messageCb );
ros::Publisher chatter("chatter", &str_msg);
String output;

void setup(){
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub);
//  Serial.begin(9600);
  if (!LoRa.begin(915E6)) {
//    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop(){
  // publish the string
  unsigned long currentTime = 0;
  unsigned long lastPublishTime = 0;
  while (1){
    nh.spinOnce();
    // create a JSON document using the ArduinoJson library
    StaticJsonDocument<200> doc;
    doc["a"] = msg.w;
    doc["b"] = msg.a;
    doc["c"] = msg.s;
    doc["d"] = msg.d;
    doc["e"] = msg.q;
    doc["f"] = msg.e;
    doc["g"] = msg.z;
    doc["h"] = msg.x;
    doc["i"] = msg.c;
    doc["j"] = msg.key_left_shift;
    doc["k"] = msg.key_left_ctrl;
    doc["l"] = msg.key_left;
    doc["m"] = msg.key_right;
  
    //need to clear output here
    output="";
    serializeJson(doc, output);
    output += "u";
    str_msg.data = output.c_str();
    chatter.publish( &str_msg );
  
    bits bit;
    bit.x = 0;
    currentTime = millis();
    if (currentTime - lastPublishTime >= 250) { // the time decides the frequency of transmisison
      str_msg.data = "Transmitting";
      chatter.publish( &str_msg );
      LoRa.beginPacket();
      LoRa.print(output);
      LoRa.endPacket();
      lastPublishTime = currentTime;
    }
  }
}
