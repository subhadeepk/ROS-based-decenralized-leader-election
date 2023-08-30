# Decentralized leader election framework built on ROS Noetic



## See if it works right away:

1. Download the repository and place it inside the src folder of your catkin
2. Find Power_state.msg in customs/msg and send.votes.srv in customs/srv. Move them to the appropriate folder and modify CMakeLists.txt and package.xml accordingly. Here's a short tutorial on how to create and custom messages and services to your package : [ros wiki tutorial]. (http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv)
3. Go to the downloaded folder and make the files executable.
4. Go to the params folder and modify the number of nodes you want to simulate.
5. Open the terminal inside the folder and run `./run.sh`.




## What does the simulation do?

It simulates n rosnodes that interact with eachother using ROS services.  Random fitness values are assigned to each node and the node with the highest fitness values is elected as the leader. They elect a new leader using an algorithm demonstrated by the the following pseudocode:

![LE_election](https://github.com/wickedticket/ROS-based-decenralized-leader-election/assets/109573774/435bfb59-36fc-496a-a5ed-13a6a1803734)

This algorithm was made for a swarm of drones which will have to elect a new leader once the old leader goes offline. You can learn more about the framework [here]([https://drive.google.com/file/d/129GMESgDbCwmpxd7BE9MdZqJg7M6vLed/view?usp=sharing](https://drive.google.com/file/d/1jBwFLMGLtu8kBb30ZzUUzeQs5LKzyFc6/view))

## Using it for your own multi-robot framework

In the simulation, main_script.py initializes every node. To run this on an independent node, you'd have to run node.py on it after changing all the parameters inside node.py. 

## NOTE
The code is not clean but it should work. Feel free to reach out if you have any suggestions or ideas for improving this framework. Discord: crimsonblues3667  Email:ksubhadeepwork@gmail.com

