#!/usr/bin/env python3
# https://github.com/Rakee003/Turtlesim_Catch-and-catch/blob/main/catch_and_catch/nodes/main.py

'''
Created on Wednesday June 30
@author : Rakesh Kumar (Modified for user coordinate input)
'''

# Required Libraries
####################
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import turtlesim.srv


class Catch_Bot:

    def __init__(self):
        rospy.init_node('catch_and_catch', anonymous=True)

        # Publisher - '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # Subscriber - '/turtle1/pose'.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.pose_refresh)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def main(self):
        self.Catcher()  # Calling the Catcher logic function

    def Catcher(self):  # Catcher logic
        goal_pose = Pose()

        while not rospy.is_shutdown():
            # User input for spawning turtle2
            try:
                goal_pose.x = float(input("Set your X coordinate for turtle2 (0.5 - 10.5): "))
                goal_pose.y = float(input("Set your Y coordinate for turtle2 (0.5 - 10.5): "))
            except ValueError:
                print("Invalid input! Please enter numbers only.")
                continue

            distance_tolerance = 0.5  # Tolerance limit for turtle1

            # Spawn turtle2 at the user's chosen coordinates
            self.Turtle_spawn(goal_pose, 'turtle1', 'turtle2')

            vel_msg = Twist()

            while self.euclidean_distance(goal_pose) >= float(distance_tolerance) and not rospy.is_shutdown():
                # Proportional controller
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

            # Stop turtle1 after reaching turtle2
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

            # Kill turtle2 after it is caught
            self.Turtle_kill('turtle2')
            print("Caught turtle2!\n")

    ############################################################################
    # Supporting Functions
    ######################

    def Turtle_spawn(self, goal, killer_name, spawn_name):
        rospy.wait_for_service('spawn')
        self.spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
        self.turtle_name = rospy.get_param(killer_name, spawn_name)
        self.spawner(goal.x, goal.y, 0, self.turtle_name)

    def Turtle_kill(self, killer_name):
        rospy.wait_for_service('kill')
        self.killer = rospy.ServiceProxy('kill', turtlesim.srv.Kill)
        self.killer(killer_name)

    def pose_refresh(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 6)
        self.pose.y = round(self.pose.y, 6)

    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=8):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)


################################################################################
# Main Program Execution
########################

if __name__ == '__main__':
    try:
        x = Catch_Bot()
        x.main()
    except rospy.ROSInterruptException:
        pass
