#!/usr/bin/env python

'''
'''
import roslib
import rospy
import sys
import cv2
import numpy as np
import time
import math
import imutils

from geometry_msgs.msg import Twist, Point
from std_msgs.msg import String
from sensor_msgs.msg import Image
PI = 3.1415926535897

class ROS:

	def __init__(self,result):
		self.pub_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
		
		self.img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
		self.move = False
		
		self.angle = 0
		self.relative_angle = self.angle
		self.speed = 0.3
		self.command = result
	
	def count(self, count):
		self.move = True
		distance = 2
		self.angle = 180
		self.relative_angle = self.angle**2*PI/360
		
		i=0		
		while(i<count):
			self.forward(distance)
			self.turn()
			i+=1
		
		self.move = False	
			
	def forward (self, distance):
		print("F")
		vel = Twist()
		vel.linear.x = self.speed
		t0 = rospy.Time.now().to_sec()
		current_distance=0

		while(current_distance < distance):
			self.pub_vel.publish(vel)
			t1=rospy.Time.now().to_sec()
			current_distance= self.speed*(t1-t0)
			
		vel.linear.x = 0
		self.pub_vel.publish(vel)
		
	def turn(self):		
		vel = Twist()
		vel.angular.z = self.speed
		t0 = rospy.Time.now().to_sec()
		current_angle=0

		while(current_angle < self.relative_angle):
			self.pub_vel.publish(vel)
			t1 = rospy.Time.now().to_sec()
			current_angle = self.speed*(t1-t0)

		vel.angular.z=0
		self.pub_vel.publish(vel)
	
	def spin(self):
		self.angle = 360
		self.relative_angle = self.angle**2*PI/360
		self.turn()

	def move_condition(self):
		print(self.command)
		if self.command == "go_back":
			self.forward(-2)
			print("g")

		elif self.command == "fetch":
			self.forward(3)
			self.forward(-3)
			print("f")

		elif self.command == "go":
			self.forward(3)
			print("G")

		elif self.command == "left":
			self.angle = 90
			self.relative_angle = self.angle**2*PI/360
			self.turn()
			self.forward(3)
			print("l")

		elif self.command == "right":
			self.angle = -90
			self.relative_angle = self.angle**2*PI/360
			self.turn()
			self.forward(3)
			print("r")

		elif self.command == "spin":
			self.spin()
			print("sp")

		elif self.command == 'stop':
			self.forward(1)
			print("s")

def main():
	rospy.init_node('image_converter', anonymous=True)
	with open("file.txt","r") as f:
		result = f.read(1)
	print(result)
	ros = ROS("stop")
	rate = rospy.Rate(10)
	try:
		ros.move_condition()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()

