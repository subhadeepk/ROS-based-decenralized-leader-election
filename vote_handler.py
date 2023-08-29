#!/usr/bin/env python3
#Rate_controller for topic B any drone 

import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import rospy
from custom_msgs.msg import Class_B, Upper_layer_setpoint, Power_state
from geometry_msgs.msg import PoseStamped, TwistStamped, AccelWithCovarianceStamped
from sensor_msgs.msg import Imu, NavSatFix
from nav_msgs.msg import Odometry
from mavros_msgs.msg import PositionTarget, HomePosition, State
from custom_msgs.srv import send_votes,send_votesResponse
from time import sleep
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Quaternion, TwistStamped, PoseStamped, Twist
from geometry_msgs.msg import Vector3
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
from array import *
import subprocess
import string as st
import threading
import time
import random

class Handle_votes():

    def __init__(self,my_signature):
        self.signature = my_signature
        self.update_local_variables()
        rospy.init_node(f'handle_votes_node_{self.my_no}')
        s = rospy.Service(f'send_votes_to_{self.my_no}', send_votes, self.handle_vote)
        rospy.Timer(rospy.Duration(0.01),self.update_local_variables)
        rospy.spin()
    
    def handle_vote(self,req):
        self.update_local_variables()
        #####print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
        ###print("received vote request")
        ##print("request received",self.my_no,req)
        ##print("my number",self.my_no,"my role",self.signature.get_role(),"fitness",self.signature.get_fitness())
        ##print(req.fitness<self.signature.get_fitness(),self.signature.get_term()==req.term,self.signature.get_role()=="Voter")
        if(req.fitness<self.signature.get_fitness())and(self.signature.get_term()==req.term)and(self.signature.get_role()=="Voter"):
            ##print("entered handler")
            #check if vote_list dictionary has term entry and add or append entry accordingly
            self.signature.update_votelist(req.votelist)
            #print(self.my_no," - node no","votes received-",len(self.signature.get_votes_in_term()),"needed",self.signature.get_no_of_nodes()-1)
            if(len(self.signature.get_votes_in_term())==self.signature.get_no_of_nodes()-1):
               print("becoming leader",self.my_no)
               self.signature.update_role("Leader")
               self.signature.update_term(self.signature.get_term() + 1)

            ##print("accepting votes",self.my_no)   
            return send_votesResponse(1) #response code 1 == Vote accepted
        else:
            return send_votesResponse(0)  #response code 0 == Vote rejected
    
    def update_local_variables(self,event=None):
        self.my_no = self.signature.get_id()
        self.term = self.signature.get_term()
        self.no_of_nodes = self.signature.get_no_of_nodes()
        self.my_role = self.signature.get_role()
        self.fitness = self.signature.get_fitness()
        self.vote_list = self.signature.get_votelist()
        