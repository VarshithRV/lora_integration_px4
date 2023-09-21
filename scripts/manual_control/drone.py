# drone module with all the methods

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBoolRequest, SetModeRequest, SetMavFrameRequest
from mavros_msgs.srv import CommandBool, SetMode, SetMavFrame, CommandTOL, CommandTOLRequest, CommandTOLResponse
from mavros_msgs.msg import State
from px4_controller.msg import key
from geometry_msgs.msg import TwistStamped
import numpy as np, threading, time
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from px4_controller.msg import drone

class Drone:
    def __init__(self):
        self.local_position = PoseStamped
        self.keyboard_input = key()
        self.velocity_vector = np.zeros((4,))
        self.mav_frame = SetMavFrameRequest()
        self.mav_frame.mav_frame = 8
        self.state = State()
        self.kill_sig = 0
        self.takeoff_altitude = 2
        self.global_position = NavSatFix()
        self.yaw = Float64()
        self.drone_ip = drone() #will contain the rpty values

    def init_self(self):
        rospy.init_node("Controller")

    def joycb(self,msg: Joy):
        self.drone_ip.thrust = msg.axes[1]
        self.drone_ip.yaw = msg.axes[0]
        self.drone_ip.roll = msg.axes[3]
        self.drone_ip.pitch = msg.axes[4]

    def dead_zone_cover(self):
        hold_vel = TwistStamped()
        pub_vel = rospy.Publisher("/mavros/local_position/cmd_vel",TwistStamped,queue_size=10)
        rate = rospy.Rate(20)
        # publish the hold_vel
        while not rospy.is_shutdown():
            if self.kill_sig:
                break
            else:
                pub_vel.publish(hold_vel)
            rate.sleep()
    
    def keycb(self,msg: key):
        self.keyboard_input = msg
        self.velocity_vector[0] = (self.keyboard_input.w - self.keyboard_input.s )
        self.velocity_vector[1] = (self.keyboard_input.a - self.keyboard_input.d )
        self.velocity_vector[2] = (self.keyboard_input.key_left_shift - self.keyboard_input.key_left_ctrl )
        self.velocity_vector[3] = (self.keyboard_input.key_left - self.keyboard_input.key_right)

    def posecb(self,msg: PoseStamped):
        self.local_position = msg

    def statecb(self,msg : State):
        self.state = msg
    
    def gpscb(self,msg: NavSatFix):
        self.global_position = msg

    def yawcb(self,msg : Float64):
        self.yaw = msg

    def manual_keyboard_control(self):
        #### Deadzone start
        rospy.init_node("Controller", disable_signals=True, anonymous=False)
        ### Deadzone cover
        self.kill_sig = 0
        dead_zone_thread = threading.Thread(target=self.dead_zone_cover,daemon=True)
        dead_zone_thread.start()

        sub=rospy.Subscriber("/keyboard",key,callback=self.keycb)
        # check_keyboard_thread = threading.Thread(target=check_keyboard,daemon=True)
        # check_keyboard_thread.start()
        sub2 = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=self.posecb)
        sub_state = rospy.Subscriber("/mavros/state",State,callback=self.statecb)
        pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
        rospy.wait_for_message("/mavros/state",State)

        velocity_sp = TwistStamped()
        rate = rospy.Rate(20)

        if not self.state.armed:
            rospy.logerr("UnArmed! control denied")
            exit()

        # set to offboard mode if not already
        if not self.state.armed or self.state.mode != "OFFBOARD":
            if not self.state.armed:
                rospy.logerr("Vehicle not armed")
                exit()
            if self.state.mode != "OFFBOARD":
                rospy.logerr("Vehicle mode is not OFFBOARD")
                # set to offboard mode
                for i in range(50):
                    pub_vel.publish(velocity_sp)
                    rate.sleep()
                rospy.wait_for_service("/mavros/set_mode")
                offb = SetModeRequest()
                offb.custom_mode = "OFFBOARD"
                set_mode = rospy.ServiceProxy("/mavros/set_mode",SetMode)
                try : 
                    set_mode.call(offb)
                except rospy.ServiceException:
                    rospy.logerr("Mode could not be set to offboard, landing")
                    exit()


        # set frame to body frame if not already
        frame = rospy.get_param("/mavros/setpoint_velocity/mav_frame")
        if frame != "BODY_NED":
            rospy.logwarn("Frame is not BODY_NED")
            body_frame = SetMavFrameRequest()
            body_frame.mav_frame = SetMavFrameRequest.FRAME_BODY_NED
            rospy.wait_for_service("/mavros/setpoint_velocity/mav_frame")
            set_body = rospy.ServiceProxy("/mavros/setpoint_velocity/mav_frame",SetMavFrame)
            try : 
                set_body.call(body_frame)
            except rospy.ServiceException:
                rospy.logerr("Frame not set to body NED")
                exit()

        self.kill_sig = 1
        dead_zone_thread.join()

        ##### Deadzone end, publishing velocity

        pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
        velocity_sp = TwistStamped()
        rospy.loginfo("Start velocity control using keyboard")
        while not rospy.is_shutdown():
            try:
                velocity_sp.twist.linear.x = self.velocity_vector[0]
                velocity_sp.twist.linear.y = self.velocity_vector[1]
                velocity_sp.twist.linear.z = self.velocity_vector[2]
                velocity_sp.twist.angular.z = self.velocity_vector[3]
                pub_vel.publish(velocity_sp)
                rate.sleep()
            except KeyboardInterrupt:
                self.mav_frame.mav_frame = 1
                # set frame to body frame
                rospy.loginfo("Keyboard interrupt detected, going back to local NED frame")
                rospy.wait_for_service("/mavros/setpoint_velocity/mav_frame")
                body_frame = rospy.ServiceProxy("/mavros/setpoint_velocity/mav_frame",SetMavFrame)
                try : 
                    body_frame.call(self.mav_frame)
                except rospy.ServiceException:
                    rospy.loginfo("Body frame denied.")
    ## Uncomment arm check before deployment
    def takeoff(self):
        rospy.init_node("Controller", disable_signals=True, anonymous=False)
        time = rospy.get_time()

        rospy.Subscriber("/mavros/local_position/pose",PoseStamped,callback=self.posecb)
        rospy.Subscriber("mavros/state",State,callback=self.statecb)
        pub = rospy.Publisher("/mavros/setpoint_position/local",PoseStamped,queue_size=10)
        rospy.wait_for_message("/mavros/local_position/pose",PoseStamped)
        rospy.wait_for_message("/mavros/state",State)
        pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
        velocity_sp = TwistStamped()
        rate = rospy.Rate(20)
        
        
        
        ###################################################### uncomment this before deployment ###########################################
        if not self.state.armed:
            rospy.logerr("Denied! Vehicle is Disarmed")
            exit()
        ###################################################################################################################################
        
        rospy.loginfo(f"Takeoff altitude = {self.takeoff_altitude}")
        rospy.loginfo("Switching to offboard in posctl")

        setpoint_position = PoseStamped()
        setpoint_position = self.local_position
        setpoint_position.pose.position.z += 2
        rospy.wait_for_message("/mavros/local_position/pose",PoseStamped)

        # set to offboard mode
        rospy.loginfo("Setting to offboard moode")
        
        if not self.state.armed or self.state.mode != "OFFBOARD":
            if self.state.mode != "OFFBOARD":
                rospy.logerr("Vehicle mode is not OFFBOARD")
                # set to offboard mode
                for i in range(50):
                    pub_vel.publish(velocity_sp)
                    rate.sleep()
                rospy.wait_for_service("/mavros/set_mode")
                offb = SetModeRequest()
                offb.custom_mode = "OFFBOARD"
                set_mode = rospy.ServiceProxy("/mavros/set_mode",SetMode)
                try : 
                    set_mode.call(offb)
                    rospy.loginfo(f"Mode = {self.state.mode}")
                except rospy.ServiceException:
                    rospy.logerr("Mode could not be set to offboard, landing")
                    exit()

        # set frame to body frame if not already
        frame = rospy.get_param("/mavros/setpoint_velocity/mav_frame")
        if frame != "BODY_NED":
            rospy.logwarn("Frame is not BODY_NED")
            body_frame = SetMavFrameRequest()
            body_frame.mav_frame = SetMavFrameRequest.FRAME_BODY_NED
            rospy.wait_for_service("/mavros/setpoint_velocity/mav_frame")
            set_body = rospy.ServiceProxy("/mavros/setpoint_velocity/mav_frame",SetMavFrame)
            try : 
                set_body.call(body_frame)
            except rospy.ServiceException:
                rospy.logerr("Frame not set to body NED")
                exit()
            
        
        # taking off to 2m.
        rate = rospy.Rate(20)
        error = 0.05 # 5cm
        time = rospy.get_time()
        while not rospy.is_shutdown() and self.local_position.pose.position.z < self.takeoff_altitude - error and rospy.get_time() - time < 10.0:
            pub.publish(setpoint_position)
            rate.sleep()
        
        rospy.loginfo(f"Altitude = {self.local_position.pose.position.z}, Takeoff altitude reached")
        rospy.loginfo(f"Time taken = {rospy.get_time()-time}")

        # velocity hold in offboard mode
        velocity_sp = TwistStamped()
        pub_vel = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)
        rospy.loginfo("Velocity hold")
        while not rospy.is_shutdown():
            pub_vel.publish(velocity_sp)
            rate.sleep()

    def land(self):
        rospy.init_node("Controller", disable_signals=True, anonymous=False)
        rospy.Subscriber("/mavros/global_position/global",NavSatFix,callback=self.gpscb)    
        rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,callback=self.yawcb)
        rospy.Subscriber("/mavros/state",State,callback=self.statecb)
        rospy.wait_for_message("/mavros/global_position/global",NavSatFix)
        rospy.wait_for_message("/mavros/global_position/compass_hdg",Float64)
        rospy.wait_for_message("/mavros/state",State)
        rospy.wait_for_service("/mavros/cmd/land")

        if not self.state.armed:
            rospy.logerr("Diarmed, already landed!")
            exit()

        msg = CommandTOLRequest()
        takeoff = rospy.ServiceProxy("/mavros/cmd/land",CommandTOL)
        response = CommandTOLResponse()

        rospy.loginfo("Landing request")
        while not rospy.is_shutdown() and self.state.mode != "AUTO.LAND":
            try : 
                response = takeoff.call(msg)
            except rospy.ServiceException:
                rospy.loginfo("Service exception")
        if response.success :
            rospy.loginfo(f"Landing successful")
        else : 
            rospy.logerr("Landing denied, check px4 logs")

        # change to auto.loiter mode after landing
        rospy.wait_for_service("/mavros/set_mode")
        guided_disarmed = SetModeRequest()
        guided_disarmed.base_mode = SetModeRequest.MAV_MODE_GUIDED_DISARMED
        setMode = rospy.ServiceProxy("/mavros/set_mode",SetMode)
        try :
            setMode.call(guided_disarmed)
        except rospy.ServiceException:
            rospy.logerr("Mode could not be set to preflight, landing")
            exit()
        rospy.loginfo("Mode set to guided_disarmed, landing successful")

    def arm(self):
        # Deadzone start
        rospy.init_node("Controller", disable_signals=True, anonymous=False)
        rospy.loginfo("Arming the drone")
        self.kill_sig = 0
        rospy.wait_for_service("/mavros/cmd/arming")
        rospy.wait_for_message("/mavros/state",State)
        rospy.Subscriber("/mavros/state",State,callback=self.statecb)
        msg = CommandBoolRequest()
        msg.value = True
        arm = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
        rate = rospy.Rate(20)
        time = rospy.get_time()
        while (not self.state.armed) and (not rospy.is_shutdown()) and (rospy.get_time() - time < 5.0):
            try : 
                arm.call(msg)
            except rospy.ServiceException:
                rospy.logerr("Arming failed, Service exception")
        rospy.loginfo(f"Arming_status = {self.state.armed}")
        if not self.state.armed:
            rospy.logerr("Arming Failed!, check px4 logs")
        else : 
            rospy.loginfo("Armed and ready")
        # Deadzone end reap the thread
        self.kill_sig = 1

    def disarm(self):
        rospy.init_node("Controller", disable_signals=True, anonymous=False)
        rospy.wait_for_service("/mavros/cmd/arming")
        rospy.Subscriber("/mavros/state",State,callback=self.statecb)
        rospy.wait_for_message("/mavros/state",State)
        msg = CommandBoolRequest()
        msg.value = False
        arm = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
        rate = rospy.Rate(20)
        time = rospy.get_time()
        while (not self.state.armed) and (not rospy.is_shutdown()) and (rospy.get_time() - time < 5.0):
            try : 
                arm.call(msg)
            except rospy.ServiceException:
                rospy.logerr("disarming failed, Service exception")
        rospy.loginfo(f"Arm = {self.state.armed}")
        if self.state.armed:
            rospy.logerr("Disarming Failed!, check px4 logs")
        else : 
            rospy.loginfo("Disarmed")

    def joy_stick_control(self):
        rospy.init_node("Controller", disable_signals=True, anonymous=False)
        rospy.Subscriber("/joy",Joy,callback=self.joycb)
        pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped",Twist,queue_size=10)
        cmd_vel = Twist()

        rospy.loginfo("Establishing joystick control")
        rate = rospy.Rate(20)

        while not rospy.is_shutdown():
            cmd_vel.linear.z=3*self.drone_ip.thrust
            cmd_vel.angular.z =3*self.drone_ip.yaw
            cmd_vel.linear.x = 3*self.drone_ip.pitch
            cmd_vel.linear.y = 3*self.drone_ip.roll
            pub.publish(cmd_vel)
            rate.sleep()