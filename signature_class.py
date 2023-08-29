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

class Node_signature:
    def __init__(self,number,term,no_of_nodes,role,fitness,vlist):
        self.number = number
        self.term = term 
        self.no_of_nodes = no_of_nodes
        self.role = role
        self.fitness = fitness
        self.vote_list = vlist

    def update_role(self,new_role):
        self.role = new_role

    def update_term(self,new_term):
        self.term = new_term
        new_entry = {self.term:list()}
        self.vote_list.update(new_entry)
    
    def update_votelist(self,votes):
        if self.term in self.vote_list.keys():
            existing_votes = self.vote_list[self.term]
            for i in votes:
                existing_votes.append(i)
            self.vote_list[self.term]=existing_votes
        # else:
        #     new_entry = {self.term:votes}
        #     self.vote_list.update(new_entry)

    def update_number_of_nodes(self):
        self.no_of_nodes = self.no_of_nodes - 1

    def get_role(self):
        return(self.role)
    
    def get_term(self):
        return(self.term)
    
    def get_fitness(self):
        return(self.fitness)
    
    def get_votes_in_term(self):
        if self.term in self.vote_list.keys():
            #print(self.number,"votes in term",self.vote_list[self.term])
            return(self.vote_list[self.term])
        else:
            return(list())
    
    def get_votelist(self):
        return(self.vote_list)
    
    def get_id(self):
        return(self.number)
    
    def get_no_of_nodes(self):
        return(self.no_of_nodes)
    