#ifndef _ROS_collision_detection_key_h
#define _ROS_collision_detection_key_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace collision_detection
{

  class key : public ros::Msg
  {
    public:
      typedef int32_t _key_up_type;
      _key_up_type key_up;
      typedef int32_t _key_down_type;
      _key_down_type key_down;
      typedef int32_t _key_left_type;
      _key_left_type key_left;
      typedef int32_t _key_right_type;
      _key_right_type key_right;
      typedef int32_t _key_left_shift_type;
      _key_left_shift_type key_left_shift;
      typedef int32_t _key_left_ctrl_type;
      _key_left_ctrl_type key_left_ctrl;
      typedef int32_t _w_type;
      _w_type w;
      typedef int32_t _a_type;
      _a_type a;
      typedef int32_t _s_type;
      _s_type s;
      typedef int32_t _d_type;
      _d_type d;
      typedef int32_t _q_type;
      _q_type q;
      typedef int32_t _e_type;
      _e_type e;
      typedef int32_t _c_type;
      _c_type c;
      typedef int32_t _x_type;
      _x_type x;
      typedef int32_t _z_type;
      _z_type z;
      typedef int32_t _j_type;
      _j_type j;

    key():
      key_up(0),
      key_down(0),
      key_left(0),
      key_right(0),
      key_left_shift(0),
      key_left_ctrl(0),
      w(0),
      a(0),
      s(0),
      d(0),
      q(0),
      e(0),
      c(0),
      x(0),
      z(0),
      j(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_key_up;
      u_key_up.real = this->key_up;
      *(outbuffer + offset + 0) = (u_key_up.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_key_up.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_key_up.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_key_up.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->key_up);
      union {
        int32_t real;
        uint32_t base;
      } u_key_down;
      u_key_down.real = this->key_down;
      *(outbuffer + offset + 0) = (u_key_down.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_key_down.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_key_down.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_key_down.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->key_down);
      union {
        int32_t real;
        uint32_t base;
      } u_key_left;
      u_key_left.real = this->key_left;
      *(outbuffer + offset + 0) = (u_key_left.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_key_left.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_key_left.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_key_left.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->key_left);
      union {
        int32_t real;
        uint32_t base;
      } u_key_right;
      u_key_right.real = this->key_right;
      *(outbuffer + offset + 0) = (u_key_right.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_key_right.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_key_right.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_key_right.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->key_right);
      union {
        int32_t real;
        uint32_t base;
      } u_key_left_shift;
      u_key_left_shift.real = this->key_left_shift;
      *(outbuffer + offset + 0) = (u_key_left_shift.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_key_left_shift.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_key_left_shift.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_key_left_shift.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->key_left_shift);
      union {
        int32_t real;
        uint32_t base;
      } u_key_left_ctrl;
      u_key_left_ctrl.real = this->key_left_ctrl;
      *(outbuffer + offset + 0) = (u_key_left_ctrl.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_key_left_ctrl.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_key_left_ctrl.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_key_left_ctrl.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->key_left_ctrl);
      union {
        int32_t real;
        uint32_t base;
      } u_w;
      u_w.real = this->w;
      *(outbuffer + offset + 0) = (u_w.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_w.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_w.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_w.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->w);
      union {
        int32_t real;
        uint32_t base;
      } u_a;
      u_a.real = this->a;
      *(outbuffer + offset + 0) = (u_a.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_a.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_a.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_a.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->a);
      union {
        int32_t real;
        uint32_t base;
      } u_s;
      u_s.real = this->s;
      *(outbuffer + offset + 0) = (u_s.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_s.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_s.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_s.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->s);
      union {
        int32_t real;
        uint32_t base;
      } u_d;
      u_d.real = this->d;
      *(outbuffer + offset + 0) = (u_d.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_d.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_d.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_d.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->d);
      union {
        int32_t real;
        uint32_t base;
      } u_q;
      u_q.real = this->q;
      *(outbuffer + offset + 0) = (u_q.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_q.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_q.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_q.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->q);
      union {
        int32_t real;
        uint32_t base;
      } u_e;
      u_e.real = this->e;
      *(outbuffer + offset + 0) = (u_e.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_e.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_e.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_e.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->e);
      union {
        int32_t real;
        uint32_t base;
      } u_c;
      u_c.real = this->c;
      *(outbuffer + offset + 0) = (u_c.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_c.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_c.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_c.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->c);
      union {
        int32_t real;
        uint32_t base;
      } u_x;
      u_x.real = this->x;
      *(outbuffer + offset + 0) = (u_x.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_x.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_x.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_x.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->x);
      union {
        int32_t real;
        uint32_t base;
      } u_z;
      u_z.real = this->z;
      *(outbuffer + offset + 0) = (u_z.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_z.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_z.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_z.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->z);
      union {
        int32_t real;
        uint32_t base;
      } u_j;
      u_j.real = this->j;
      *(outbuffer + offset + 0) = (u_j.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_j.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_j.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_j.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->j);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      union {
        int32_t real;
        uint32_t base;
      } u_key_up;
      u_key_up.base = 0;
      u_key_up.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_key_up.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_key_up.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_key_up.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->key_up = u_key_up.real;
      offset += sizeof(this->key_up);
      union {
        int32_t real;
        uint32_t base;
      } u_key_down;
      u_key_down.base = 0;
      u_key_down.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_key_down.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_key_down.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_key_down.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->key_down = u_key_down.real;
      offset += sizeof(this->key_down);
      union {
        int32_t real;
        uint32_t base;
      } u_key_left;
      u_key_left.base = 0;
      u_key_left.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_key_left.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_key_left.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_key_left.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->key_left = u_key_left.real;
      offset += sizeof(this->key_left);
      union {
        int32_t real;
        uint32_t base;
      } u_key_right;
      u_key_right.base = 0;
      u_key_right.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_key_right.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_key_right.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_key_right.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->key_right = u_key_right.real;
      offset += sizeof(this->key_right);
      union {
        int32_t real;
        uint32_t base;
      } u_key_left_shift;
      u_key_left_shift.base = 0;
      u_key_left_shift.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_key_left_shift.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_key_left_shift.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_key_left_shift.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->key_left_shift = u_key_left_shift.real;
      offset += sizeof(this->key_left_shift);
      union {
        int32_t real;
        uint32_t base;
      } u_key_left_ctrl;
      u_key_left_ctrl.base = 0;
      u_key_left_ctrl.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_key_left_ctrl.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_key_left_ctrl.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_key_left_ctrl.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->key_left_ctrl = u_key_left_ctrl.real;
      offset += sizeof(this->key_left_ctrl);
      union {
        int32_t real;
        uint32_t base;
      } u_w;
      u_w.base = 0;
      u_w.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_w.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_w.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_w.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->w = u_w.real;
      offset += sizeof(this->w);
      union {
        int32_t real;
        uint32_t base;
      } u_a;
      u_a.base = 0;
      u_a.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_a.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_a.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_a.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->a = u_a.real;
      offset += sizeof(this->a);
      union {
        int32_t real;
        uint32_t base;
      } u_s;
      u_s.base = 0;
      u_s.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_s.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_s.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_s.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->s = u_s.real;
      offset += sizeof(this->s);
      union {
        int32_t real;
        uint32_t base;
      } u_d;
      u_d.base = 0;
      u_d.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_d.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_d.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_d.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->d = u_d.real;
      offset += sizeof(this->d);
      union {
        int32_t real;
        uint32_t base;
      } u_q;
      u_q.base = 0;
      u_q.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_q.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_q.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_q.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->q = u_q.real;
      offset += sizeof(this->q);
      union {
        int32_t real;
        uint32_t base;
      } u_e;
      u_e.base = 0;
      u_e.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_e.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_e.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_e.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->e = u_e.real;
      offset += sizeof(this->e);
      union {
        int32_t real;
        uint32_t base;
      } u_c;
      u_c.base = 0;
      u_c.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_c.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_c.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_c.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->c = u_c.real;
      offset += sizeof(this->c);
      union {
        int32_t real;
        uint32_t base;
      } u_x;
      u_x.base = 0;
      u_x.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_x.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_x.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_x.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->x = u_x.real;
      offset += sizeof(this->x);
      union {
        int32_t real;
        uint32_t base;
      } u_z;
      u_z.base = 0;
      u_z.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_z.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_z.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_z.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->z = u_z.real;
      offset += sizeof(this->z);
      union {
        int32_t real;
        uint32_t base;
      } u_j;
      u_j.base = 0;
      u_j.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_j.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_j.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_j.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->j = u_j.real;
      offset += sizeof(this->j);
     return offset;
    }

    virtual const char * getType() override { return "collision_detection/key"; };
    virtual const char * getMD5() override { return "a26683c11d1762afa274bfb0bab8b879"; };

  };

}
#endif
