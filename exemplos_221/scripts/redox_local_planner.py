#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import  Odometry, Path
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseStamped, Point
from math import atan2, inf, sqrt, degrees
x = 0
y = 0
theta = 0
alpha = 0
poses = []

def euclidean_distance(point1, point2):
    a = abs(point1[0] - point2[0])**2
    b = abs(point1[1] - point2[1])**2
    return sqrt(a + b)

def dot_product(point1, point2):
    a = point1[0] * point2[0]
    b = point1[1] * point2[1]
    return a + b

def vector_magnitude(vector):
    a = vector[0]**2
    b = vector[1]**2
    return sqrt(a + b)

def recebeu_odom(dado):
    global x
    global y 
    global theta
    x = dado.pose.pose.position.x
    y = dado.pose.pose.position.y
    ora_q = dado.pose.pose.orientation
    (roll,pitch,theta) = euler_from_quaternion([ora_q.x,ora_q.y,ora_q.z,ora_q.w])

def recebeu_path(dado):
    global poses
    poses = dado.poses

def getAlpha(x, y, theta, alpha_curr, raio_robo, poses):
    point1 = [x, y]
    point2 = [inf, inf]
    dist_atual = inf
    for pose in poses:
        point_candidate = [pose.pose.position.x, pose.pose.position.y]
        dist_candidate = euclidean_distance(point1, point_candidate)
        if abs(dist_candidate - raio_robo) < abs(dist_atual - raio_robo) and dist_candidate > raio_robo:
            point2 = point_candidate
            dist_atual = euclidean_distance(point1, point2)
    beta = atan2(point2[1] - point1[1], point2[0] - point1[0])
    alpha = degrees(beta - theta)
    if alpha < 0:
        alpha += 360
    elif alpha > 360:
        alpha -= 360
    if abs(alpha - alpha_curr) < 180:
        alpha = (0.5 * alpha) + (0.5 * alpha_curr)
    return alpha
    
def getVel(alpha,k):
    vel = Twist()
    if alpha <= k or alpha >= (360 - k):
        vel.linear.x = 0.2
    elif (alpha < 90 and alpha > k) or (alpha > (180 + k) and alpha < 270):
        vel.angular.z = 0.4
    elif (alpha >= (180 - k) and alpha <= (180 + k)):
        vel.linear.x = -0.2
    else:
        vel.angular.z = -0.4
    return vel  


if __name__=="__main__":
    rospy.init_node("redox_local_planner")
    topic_odom = rospy.Subscriber("/odom", Odometry , recebeu_odom)
    topic_voronoi = rospy.Subscriber("/roda/VoronoiPlanner/plan", Path, recebeu_path)
    topic_vel = rospy.Publisher('/cmd_vel',Twist)
    rospy.sleep(10)
    while not rospy.is_shutdown():
        alpha = getAlpha(x, y, theta, alpha, 0.3, poses)
        print(alpha)
        vel = getVel(alpha,10)
        topic_vel.publish(vel)
        rospy.sleep(0.1)
        
        


