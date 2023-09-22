#ifndef _ROS_px4_controller_drone_h
#define _ROS_px4_controller_drone_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace px4_controller
{

  class drone : public ros::Msg
  {
    public:
      typedef float _pitch_type;
      _pitch_type pitch;
      typedef float _yaw_type;
      _yaw_type yaw;
      typedef float _thrust_type;
      _thrust_type thrust;
      typedef float _roll_type;
      _roll_type roll;
      typedef int32_t _servo_type;
      _servo_type servo;
      typedef int32_t _mode_type;
      _mode_type mode;
      typedef int32_t _arm_type;
      _arm_type arm;
      typedef int32_t _disarm_type;
      _disarm_type disarm;
      typedef int32_t _hold_type;
      _hold_type hold;
      typedef int32_t _camera_type;
      _camera_type camera;
      typedef int32_t _kill_type;
      _kill_type kill;

    drone():
      pitch(0),
      yaw(0),
      thrust(0),
      roll(0),
      servo(0),
      mode(0),
      arm(0),
      disarm(0),
      hold(0),
      camera(0),
      kill(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      union {
        float real;
        uint32_t base;
      } u_pitch;
      u_pitch.real = this->pitch;
      *(outbuffer + offset + 0) = (u_pitch.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_pitch.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_pitch.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_pitch.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->pitch);
      union {
        float real;
        uint32_t base;
      } u_yaw;
      u_yaw.real = this->yaw;
      *(outbuffer + offset + 0) = (u_yaw.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_yaw.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_yaw.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_yaw.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->yaw);
      union {
        float real;
        uint32_t base;
      } u_thrust;
      u_thrust.real = this->thrust;
      *(outbuffer + offset + 0) = (u_thrust.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_thrust.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_thrust.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_thrust.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->thrust);
      union {
        float real;
        uint32_t base;
      } u_roll;
      u_roll.real = this->roll;
      *(outbuffer + offset + 0) = (u_roll.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_roll.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_roll.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_roll.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->roll);
      union {
        int32_t real;
        uint32_t base;
      } u_servo;
      u_servo.real = this->servo;
      *(outbuffer + offset + 0) = (u_servo.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_servo.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_servo.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_servo.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->servo);
      union {
        int32_t real;
        uint32_t base;
      } u_mode;
      u_mode.real = this->mode;
      *(outbuffer + offset + 0) = (u_mode.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_mode.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_mode.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_mode.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->mode);
      union {
        int32_t real;
        uint32_t base;
      } u_arm;
      u_arm.real = this->arm;
      *(outbuffer + offset + 0) = (u_arm.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_arm.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_arm.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_arm.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->arm);
      union {
        int32_t real;
        uint32_t base;
      } u_disarm;
      u_disarm.real = this->disarm;
      *(outbuffer + offset + 0) = (u_disarm.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_disarm.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_disarm.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_disarm.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->disarm);
      union {
        int32_t real;
        uint32_t base;
      } u_hold;
      u_hold.real = this->hold;
      *(outbuffer + offset + 0) = (u_hold.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_hold.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_hold.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_hold.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->hold);
      union {
        int32_t real;
        uint32_t base;
      } u_camera;
      u_camera.real = this->camera;
      *(outbuffer + offset + 0) = (u_camera.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_camera.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_camera.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_camera.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->camera);
      union {
        int32_t real;
        uint32_t base;
      } u_kill;
      u_kill.real = this->kill;
      *(outbuffer + offset + 0) = (u_kill.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_kill.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_kill.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_kill.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->kill);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      union {
        float real;
        uint32_t base;
      } u_pitch;
      u_pitch.base = 0;
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->pitch = u_pitch.real;
      offset += sizeof(this->pitch);
      union {
        float real;
        uint32_t base;
      } u_yaw;
      u_yaw.base = 0;
      u_yaw.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_yaw.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_yaw.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_yaw.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->yaw = u_yaw.real;
      offset += sizeof(this->yaw);
      union {
        float real;
        uint32_t base;
      } u_thrust;
      u_thrust.base = 0;
      u_thrust.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_thrust.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_thrust.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_thrust.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->thrust = u_thrust.real;
      offset += sizeof(this->thrust);
      union {
        float real;
        uint32_t base;
      } u_roll;
      u_roll.base = 0;
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->roll = u_roll.real;
      offset += sizeof(this->roll);
      union {
        int32_t real;
        uint32_t base;
      } u_servo;
      u_servo.base = 0;
      u_servo.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_servo.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_servo.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_servo.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->servo = u_servo.real;
      offset += sizeof(this->servo);
      union {
        int32_t real;
        uint32_t base;
      } u_mode;
      u_mode.base = 0;
      u_mode.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_mode.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_mode.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_mode.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->mode = u_mode.real;
      offset += sizeof(this->mode);
      union {
        int32_t real;
        uint32_t base;
      } u_arm;
      u_arm.base = 0;
      u_arm.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_arm.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_arm.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_arm.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->arm = u_arm.real;
      offset += sizeof(this->arm);
      union {
        int32_t real;
        uint32_t base;
      } u_disarm;
      u_disarm.base = 0;
      u_disarm.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_disarm.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_disarm.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_disarm.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->disarm = u_disarm.real;
      offset += sizeof(this->disarm);
      union {
        int32_t real;
        uint32_t base;
      } u_hold;
      u_hold.base = 0;
      u_hold.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_hold.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_hold.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_hold.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->hold = u_hold.real;
      offset += sizeof(this->hold);
      union {
        int32_t real;
        uint32_t base;
      } u_camera;
      u_camera.base = 0;
      u_camera.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_camera.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_camera.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_camera.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->camera = u_camera.real;
      offset += sizeof(this->camera);
      union {
        int32_t real;
        uint32_t base;
      } u_kill;
      u_kill.base = 0;
      u_kill.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_kill.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_kill.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_kill.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->kill = u_kill.real;
      offset += sizeof(this->kill);
     return offset;
    }

    virtual const char * getType() override { return "px4_controller/drone"; };
    virtual const char * getMD5() override { return "20e18abf75dd59181084f6d2ac41ceb1"; };

  };

}
#endif
