#include "ros/ros.h"
#include "std_msgs/String.h"
#include "px4_controller/key.h"
#include <sstream>

px4_controller::key key_msg;

void chatterCallback(const px4_controller::key& msg)
{
    key_msg = msg;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "talker");
  ros::NodeHandle n;
  ros::Publisher chatter_pub = n.advertise<px4_controller::key>("chatter", 1000);
  ros::Subscriber sub = n.subscribe("/demo_topic1", 1000, chatterCallback);
  ros::Rate loop_rate(10);
  int count = 0;
  std_msgs::String string_msg;
  while (ros::ok())
  {
    // chatter_pub.publish(key_msg);
    std::cout << key_msg.w << key_msg.a << key_msg.s << key_msg.d << std::endl;
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}