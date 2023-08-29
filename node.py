#!/usr/bin/env python3
#Rate_controller for topic B any drone 

import time
import rospy
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from power_handler import Leader_election 
from signature_class import Node_signature
from vote_handler import Handle_votes
import params
import random

class CustomManager(BaseManager):
    # nothing
    pass

def n1_fun(signature_log):
    a = Leader_election(signature_log)

def n2_fun(signature_log):
    b = Handle_votes(signature_log)

def main(n):
    try:
        CustomManager.register('Node_signature', Node_signature)
        with CustomManager() as manager:
            term_set = 1
            my_role_set = "Follower"
            no_of_nodes_set = params.number_of_nodes
            my_no_set = n
            my_fitness_set = random.randint(1,1000)#params.fitness[my_no_set]
            vlist = {term_set:list()} 
            my_signature = manager.Node_signature(my_no_set,term_set,no_of_nodes_set,my_role_set,my_fitness_set,vlist)
     
            p1 = Process(target=n1_fun, args=(my_signature,)) 
            p2 = Process(target=n2_fun, args=(my_signature,)) 
        
            p1.start()
            p2.start()
    
            p1.join()
            p2.join()

    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(0)
