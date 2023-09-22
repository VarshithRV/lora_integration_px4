#ifndef _ROS_px4_controller_buttons_h
#define _ROS_px4_controller_buttons_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace px4_controller
{

  class buttons : public ros::Msg
  {
    public:
      uint32_t button_length;
      typedef int32_t _button_type;
      _button_type st_button;
      _button_type * button;

    buttons():
      button_length(0), st_button(), button(nullptr)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const override
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->button_length >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->button_length >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->button_length >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->button_length >> (8 * 3)) & 0xFF;
      offset += sizeof(this->button_length);
      for( uint32_t i = 0; i < button_length; i++){
      union {
        int32_t real;
        uint32_t base;
      } u_buttoni;
      u_buttoni.real = this->button[i];
      *(outbuffer + offset + 0) = (u_buttoni.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_buttoni.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_buttoni.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_buttoni.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->button[i]);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer) override
    {
      int offset = 0;
      uint32_t button_lengthT = ((uint32_t) (*(inbuffer + offset))); 
      button_lengthT |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1); 
      button_lengthT |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2); 
      button_lengthT |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3); 
      offset += sizeof(this->button_length);
      if(button_lengthT > button_length)
        this->button = (int32_t*)realloc(this->button, button_lengthT * sizeof(int32_t));
      button_length = button_lengthT;
      for( uint32_t i = 0; i < button_length; i++){
      union {
        int32_t real;
        uint32_t base;
      } u_st_button;
      u_st_button.base = 0;
      u_st_button.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_st_button.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_st_button.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_st_button.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->st_button = u_st_button.real;
      offset += sizeof(this->st_button);
        memcpy( &(this->button[i]), &(this->st_button), sizeof(int32_t));
      }
     return offset;
    }

    virtual const char * getType() override { return "px4_controller/buttons"; };
    virtual const char * getMD5() override { return "5b447757f4e300b93c244b6afb8433e5"; };

  };

}
#endif
