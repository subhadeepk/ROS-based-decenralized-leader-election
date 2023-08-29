#!/usr/bin/env python3
# control architecture for drone i 

import numpy as np
from math import degrees
import math
import pymap3d as pm

import pygame 
import rospy
from geometry_msgs.msg import PoseStamped, TwistStamped, AccelWithCovarianceStamped
from sensor_msgs.msg import Imu
from mavros_msgs.msg import PositionTarget, HomePosition, State
from time import sleep
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Quaternion, TwistStamped, PoseStamped, Twist
from geometry_msgs.msg import Vector3
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
from array import *
import subprocess
import string as st

from custom_msgs.msg import Upper_layer_setpoint


class Base():
    def __init__(self):
        rospy.init_node('gcs_to_fury')
        self.mac = []
        self.g = 10
        my_no = 1  # set drone number
        leader_no = 3
        no_of_drones = 3
        #Initialize ros node
                #define containers for drone pos
        self.fury_1_pos = pygame.math.Vector3()
        self.fury_2_pos = pygame.math.Vector3()
        self.fury_3_pos = pygame.math.Vector3()
        
        self.gcs2fury = rospy.Publisher('gcs_to_fury',Upper_layer_setpoint,queue_size=10)

        # Publisher for the /mavros/setpoint_raw/local topic
        setpoint_raw_local_pub = rospy.Publisher(f'fury_{my_no}/mavros/setpoint_raw/local', PositionTarget, queue_size=10)

        # Set the loop rate to 10 Hz       
        rate = rospy.Rate(10)
        t = 0
        dt = 0.05

        s_a = 195
        s_b = 240

        # Set the loop rate to 10 Hz       
        rate = rospy.Rate(10)
        while (not rospy.is_shutdown()):#and(self.fury_1_pos.x):
            setpoint_A = Upper_layer_setpoint()
            setpoint_A.fury_1_x = 2
            setpoint_A.fury_1_y = 2
            self.gcs2fury.publish(setpoint_A)
            
            t += dt
            rate.sleep()

    def generate_infinity_path(self, t, length=3, width=5):
        x = length * np.sin(t)
        y = width * np.sin(t) * np.cos(t)
        return x,y 


    

if __name__ == '__main__':
    try:
        controller = Base()
    except rospy.ROSInterruptException:
        pass