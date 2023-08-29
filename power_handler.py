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
import random
import rosservice

class Leader_election():
    def __init__(self,my_signature):
        #######print('Initialized node',my_no)
        self.signature = my_signature
        self.update_local_variables()

        # self.log_length = self.log_length + 1
        # self.log_length = 0
        # self.update_log(my_signature)
        
        rospy.init_node(f"Power_of_{self.my_no}")
        self.leader_connection_threshold = 5
        self.current_motive = "Leader_follower"
        self.need_election = False
        self.time_voted = 0
        self.time_failed_to_find = 0
        neighbours_list = []
        self.counter = 0
        
        for i in range(1,self.no_of_nodes+1):
            if(i!=self.my_no):    
                neighbours_list.append(i)

        ######print(neighbours_list)
        
        self.sorted_neighbors_list = random.shuffle(neighbours_list)
            

        self.rate_high = 1
        self.time_last_active = time.time()

        #Subscribe to my state
        #rospy.Subscriber(f'fury_{self.my_no}/mavros/state', State, self.my_state_callback)
        
        # self.publish_to_centroid = rospy.Publisher('/virtual_leader',Upper_layer_setpoint,queue_size=10)
        self.publish_power_state = rospy.Publisher(f'power_state_{self.my_no}',Power_state,queue_size=10)

        rospy.Timer(rospy.Duration(1),self.publish_my_state)
        rospy.Timer(rospy.Duration(0.1),self.update_local_variables)

        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.check_alive_status()
            rate.sleep()
        # rospy.Timer(rospy.Duration(1/self.rate_high),self.check_alive_status)
        # #Make the topic and publish data  
        # #rospy.Timer(rospy.Duration(1/self.rate_high),self.publish_my_state)
        # 2
        # .rospy.spin()
            
    def run_leader_election(self):
        if True:#(self.my_role == "Voter"):
            ######print("Election time")
            #sleep(3)
            for node in range(1,self.no_of_nodes+1):
                if node!=self.my_no:
                    ######print("sending request to",node)
                    # fury_no = self.mac_vs_node_no[mac]
                    if self.send_votes_fun(node):
                        print(self.my_no,"successfully sent votes",self.list1,"to",node)
                        self.signature.update_term(self.term + 1)
                        self.vote_casted = True
                        self.signature.update_role("Voted")
                        self.time_voted = time.time()
                        self.failed_to_find = False
                        break
            if(self.signature.get_role()!="Voted"):
                print("LE ended with no result for node", self.my_no)    
                self.time_failed_to_find = time.time()
                self.failed_to_find = True

    def send_votes_fun(self, number):
        service_name = f'/send_votes_to_{number}'
        serv_list = rosservice.get_service_list()
        if (service_name in serv_list):
            try:
                ######print("sending votes")
                rospy.wait_for_service(f'send_votes_to_{number}',timeout=3)
                send = rospy.ServiceProxy(f'send_votes_to_{number}', send_votes)
                self.list1 = self.signature.get_votes_in_term()
                #print(self.my_no,"- node no list",self.list1,"list1 type",type(self.list1))
                self.list1.append(self.my_no)
                ###print(self.my_no,"sending to",number,"votes -",self.list1)
                
                resp1 = send(self.list1, self.my_no, self.fitness, self.term)
                ###print("service called", resp1.response)
                return resp1.response
            except rospy.ServiceException as e:
                #print("Service call failed: %s" % e)
                switch = False
                return 0
        else:
            #print(self.my_no,"Failed to find",number)
            self.signature.update_number_of_nodes()
            return 0
 
    def check_alive_status(self,event=None):

        if True: #self.current_state.mode=="GUIDED" and self.current_motive == "Leader_follower":
            if(self.my_role == "Leader"): #Check if gcs is publishing 
                ###print("I am leader",self.my_no)
                topic_name = '/gcs_to_fury'
                published_topics = rospy.get_published_topics()
                has_publisher = any(topic == topic_name for topic, _ in published_topics)

                if has_publisher:
                    self.has_active_publishers = True
                    rospy.loginfo(f"Leader node no. {self.my_no} has established connection with GCS: %s")
                    self.publish_to_vl()
                    #self.upper_layer_setpoint = pygame.math.Vector3(self.upper_layer_setpoint_x,self.upper_layer_setpoint_y,self.fury_1_pos.z)
                else:
                    self.publish_to_centroid.unregister()
                    self.has_active_publishers = False #does not have any active publishers.")
                    rospy.logerr(f"Leader node no. {self.my_no} cannot contact GCS: %s")
            # elif self.signature.get_role()=="Voted" and self.time_voted - time.time()<60:
            #     p = 0
            #     ##print("Role is Voted",self.my_no)
            #     #self.signature.update_role("Waiting for results")
            #     #sleep(5)
                
            #     #insert timeout feature
            #     #pass
            else:
                ######print("here")
                topic_name = f'/virtual_leader' 
                published_topics = rospy.get_published_topics()
                has_publisher = any(topic == topic_name for topic, _ in published_topics)

                if has_publisher:
                    #print("I am Follower",self.my_no)
                    self.signature.update_role("Follower")
                    self.virtual_leader_has_active_publishers = True
                    self.check_life = True 
                    self.time_last_active = time.time()

                    #self.upper_layer_setpoint = pygame.math.Vector3(self.upper_layer_setpoint_x,self.upper_layer_setpoint_y,self.fury_1_pos.z)
                else:
                    self.virtual_leader_has_active_publishers = False #does not have any active publishers.")
                    self.blind_time_elapsed = time.time()-self.time_last_active
                    time_since_last_election = time.time()-self.time_voted 
                    ####print("about to conduct election",self.blind_time_elapsed)
                    if (self.blind_time_elapsed>self.leader_connection_threshold) and (time_since_last_election>15 or (time.time()-self.time_failed_to_find)>5) :
                        #print(self.my_no,"Running LE",self.counter)
                        self.counter = self.counter + 1
                        self.signature.update_role("Voter")
                        ####print("my role",self.my_no,self.my_role)
                        self.run_leader_election()
    
    def publish_to_vl(self):
        self.publish_to_centroid = rospy.Publisher('/virtual_leader',Upper_layer_setpoint,queue_size=10)
        setpoint_A = Upper_layer_setpoint()
        setpoint_A.fury_1_x = 1
        setpoint_A.fury_1_y = 1
        ##print("node",self.my_no,"is publishing to vl")
        self.publish_to_centroid.publish(setpoint_A)

    def publish_my_state(self,event=None):
        msg = Power_state()
        msg.id = self.my_no
        msg.leader_id = 55
        msg.term = self.term
        msg.votes_recieved=self.signature.get_votes_in_term()
        #####print("vote list",self.my_no," ",self.signature.vote_list)
        ###print("Current role of",self.my_no,"is",self.signature.get_role())
        msg.fitness_value=self.fitness
        msg.role = self.my_role
        msg.motive = self.current_motive
        #####print("node 2",msg)
        self.publish_power_state.publish(msg)

    def update_local_variables(self,event=None):
        self.my_no = self.signature.get_id()
        self.term = self.signature.get_term()
        self.no_of_nodes = self.signature.get_no_of_nodes()
        self.my_role = self.signature.get_role()
        self.fitness = self.signature.get_fitness()
        self.vote_list = self.signature.get_votelist()
