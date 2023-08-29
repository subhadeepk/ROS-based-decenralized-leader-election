#!/usr/bin/env python

import rospy
import matplotlib.pyplot as plt
from geometry_msgs.msg import Point

# Define global variables to store data from ROS topics
topic_data = {
    'topic1': None,
    'topic2': None,
    'topic3': None,
    'topic4': None,
    'topic5': None
}

# ROS topic callback functions
def topic1_callback(msg):
    topic_data['topic1'] = msg

def topic2_callback(msg):
    topic_data['topic2'] = msg

def topic3_callback(msg):
    topic_data['topic3'] = msg

def topic4_callback(msg):
    topic_data['topic4'] = msg

def topic5_callback(msg):
    topic_data['topic5'] = msg

def plot_pentagon():
    # Initialize ROS node
    rospy.init_node('dynamic_pentagon_plot')

    # ROS topic subscribers
    rospy.Subscriber('topic1', Point, topic1_callback)
    rospy.Subscriber('topic2', Point, topic2_callback)
    rospy.Subscriber('topic3', Point, topic3_callback)
    rospy.Subscriber('topic4', Point, topic4_callback)
    rospy.Subscriber('topic5', Point, topic5_callback)

    plt.ion()  # Turn on interactive mode for continuous plotting
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    while not rospy.is_shutdown():
        # Check if all data from the topics are available
        if all(topic_data.values()):
            # Extract data from topic_data dictionary
            x = [topic_data['topic1'].x, topic_data['topic2'].x, topic_data['topic3'].x, topic_data['topic4'].x, topic_data['topic5'].x]
            y = [topic_data['topic1'].y, topic_data['topic2'].y, topic_data['topic3'].y, topic_data['topic4'].y, topic_data['topic5'].y]

            # Plot the points of the pentagon
            ax.clear()
            ax.plot(x + [x[0]], y + [y[0]], marker='o', linestyle='-', color='b')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            plt.draw()
            plt.pause(0.1)

        rospy.Rate(10).sleep()  # Set the loop rate to update the plot (adjust as needed)

if __name__ == "__main__":
    try:
        plot_pentagon()
    except rospy.ROSInterruptException:
        pass
