# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
import os
import sys
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

class Navigation():
	def __init__(self):
		self.goal_sent = False

		# What to do if shut down (e.g. Ctrl-C or failure)
		rospy.on_shutdown(self.shutdown)

		# Tell the action client that we want to spin a thread by default
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		rospy.loginfo("Wait for the action server to come up")

		# Allow up to 5 seconds for the action server to come up
		self.move_base.wait_for_server(rospy.Duration(5))

	def goto(self, pos, quat):

		# Send a goal
		self.goal_sent = True
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = 'map'
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
											Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

		# Start moving
		self.move_base.send_goal(goal)
		# Allow TurtleBot up to 60 seconds to complete task
		success = self.move_base.wait_for_result(rospy.Duration(60))

		state = self.move_base.get_state()
		result = False

		if success and state == GoalStatus.SUCCEEDED:
		# We made it!
			result = True
		else:
			self.move_base.cancel_goal()

		self.goal_sent = False
		return result

	def shutdown(self):
		if self.goal_sent:
			self.move_base.cancel_goal()
		rospy.loginfo("Stop")
		rospy.sleep(1)

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

def defineHome():
	home = input("Enter x and y value of coordinate of home with a space inbetween.: ")
	home = [float(i) for i in home.split(" ")]

	homeFile = open("home.txt","r+")
	if (os.path.getsize("home.txt")!=0):
		homeFile.write(str(home[0]) +" " + str(home[1]))
	else:
		homeFile.truncate()
		homeFile.write(str(home[0]) +" " + str(home[1]))
	homeFile.close()
	print("Home coordinate has been defined")
	return home

def addTables(tableList):
	tablesFile = open("tables.txt","a")
	number = int(input("How many tables would you like to add: "))
	for x in range(0,number):
		newTable = input("Enter x and y value of coordinate of next table with a space inbetween.: ")
		newTable = [float(i) for i in newTable.split(" ")]
		tableList.append(newTable)
		direction = input("Enter direction of turtlebot. U(up)/D(down)/L(left)/R(right): ")
		if direction == 'U':
			newTable.append([1,0,0,0])
		elif direction == 'D':
			newTable.append([0,0,0,-1])
		elif direction == 'L':
			newTable.append([0.7,0,0,0.7])
		elif direction == 'R':
			newTable.append([0.7,0,0,-0.7])
		
			#d 0 0 0 -1
			#u 1 0 0 0
			#l 0.7 0 0 0.7
			#r 0.7 0 0 -0.7
		tablesFile.write(str(newTable[0]) +" "+ str(newTable[1]) + " " +
		str(newTable[2][0]) + " " +
		str(newTable[2][1]) + " " +
		str(newTable[2][2]) + " " +
		str(newTable[2][3]) + "\n")
		print("Table has been saved and assigned table number "+str(len(tableList)))

	tablesFile.close()
	return tableList

def deliverTo():
	deliverTo = input("Enter what table to deliver to: ")
	deliverTo = int(deliverTo)-1

	travelTo(tableList[deliverTo])

	"""
	rospy.init_node('nav_test', anonymous=False)
	navigator = Navigation()

	# Customize the following values so they are appropriate for your location
	position = {'x': tableList[deliverTo][0], 'y' : tableList[deliverTo][1]}
	quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

	rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
	success = navigator.goto(position, quaternion)

	if success:
		rospy.loginfo("Hooray, reached the desired pose")
	else:
		rospy.loginfo("The base failed to reach the desired pose")

	# Sleep to give the last log messages time to be sent
	rospy.sleep(1)
	"""
"""
def returnHome():
	rospy.init_node('nav_test', anonymous=False)
	navigator = Navigation()

	# Customize the following values so they are appropriate for your location
	position = {'x': home[0], 'y' : home[1]}
	quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

	rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
	success = navigator.goto(position, quaternion)

	if success:
		rospy.loginfo("Hooray, reached the desired pose")
	else:
		rospy.loginfo("The base failed to reach the desired pose")

	# Sleep to give the last log messages time to be sent
	rospy.sleep(1)
"""

def travelTo(location):
	rospy.init_node('nav_test', anonymous=False)
	navigator = Navigation()

	# Customize the following values so they are appropriate for your location
	position = {'x': location[0], 'y' : location[1]}
	quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

	rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
	success = navigator.goto(position, quaternion)

	if success:
		rospy.loginfo("Hooray, reached the desired pose")
	else:
		rospy.loginfo("The base failed to reach the desired pose")

	# Sleep to give the last log messages time to be sent
	rospy.sleep(1)

def landmark(landmarkList):
	landmarkFile = open("landmarks.txt","a")
	number = int(input("How many landmarks would you like to add: "))
	for x in range(0,number):
		newLandmark = input("Enter x and y value of coordinate of next landmark with a space inbetween.: ")
		newLandmark = [float(i) for i in newLandmark.split(" ")]
		landmarkList.append(newLandmark)
		landmarkFile.write(str(newLandmark[0]) +" "+ str(newLandmark[1]) +"\n")
		print("Landmark has been saved and assigned landmark number " + str(len(landmarkList)))

	landmarkFile.close()
	return landmarkList

def moveTable(tableList):
	print("Number of tables is " +str(len(tableList)))
	tableNumber = input("Enter table you would like to move: ")
	tableNumber = int(tableNumber)
	newTable = input("Enter x and y value of coordinate of table's new location with a space inbetween.: ")
	newTable = [float(i) for i in newTable.split(" ")]
	tableList[tableNumber-1] = newTable

	tablesFile = open("tables.txt","r+")
	tablesFile.truncate()
	for table in tableList:
		tablesFile.write(str(table[0]) +" "+ str(table[1]) +"\n")
	tablesFile.close()
	print("Table "+ str(tableNumber)+" has been moved")
	return tableList

####################################################################################################################################
####################################################################################################################################
###########################################  MAIN  ##################################################################################

if __name__ == '__main__':
	dontexit = True
	tableList = []
	landmarkList = []
	home = []

	try:
		tablesFile = open("tables.txt","r+")
	except:
		tablesFile = open("tables.txt","w+")
	try:
		landmarkFile = open("landmark.txt","r+")
	except:
		landmarkFile = open("landmark.txt","w+")
	try:
		homeFile = open("home.txt","r+")
	except:
		homeFile = open("home.txt","w+")

	if (os.path.getsize("home.txt")!=0):
		home = homeFile.readline()
		home = [float(i) for i in home.split(" ")]

	if (os.path.getsize("tables.txt")!=0):
		for line in tablesFile:
			tableList.append([float(i) for i in line.split(" ")])
	tablesFile.close()
	homeFile.close()

	if (os.path.getsize("landmark.txt")!=0):
		for line in landmarkFile:
			landmarkList.append([float(i) for i in line.split(" ")])
	landmarkFile.close()

	while (dontexit):
		try:
			print()
			print("[1] DEFINEHOME: define home location")
			print("[2] ADDTABLE: add new table")
			print("[3] DELIVERTO: deliver to a table")
			print("[4] RETURNHOME: return robot home")
			print("[5] MOVETABLE: change table location")
			print("[6] ADDLANDMARKS: add new landmarks")
			print("Enter EXIT to exit")
			nextCommand = input()

			if (nextCommand == "1"):
				home = defineHome()

			elif (nextCommand == "2"):
				tableList = addTables(tableList)

			elif (nextCommand == "3"):
				moveTable(tableList)

			elif (nextCommand == "4"):
				deliverTo()

			elif (nextCommand == "5"):
				travelTo(home)

			elif (nextCommand == "2"):
				landmarkList = landmark(landmarkList)

			elif (nextCommand == "EXIT"):
				dontexit=False

		except rospy.ROSInterruptException:
			rospy.loginfo("Ctrl-C caught. Quitting")
