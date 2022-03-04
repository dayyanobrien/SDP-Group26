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
	validInput = False
	while (not validInput):
		try:
			home = input("Enter x and y value of coordinate of home with a space inbetween: ")
			home = [float(i) for i in home.split(" ")]
			validInput = len(home)==2
		except ValueError:
			validInput=False
			print("Invalid input")

	home = [float(i) for i in home]

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

	validInput = False
	while (not validInput):
		try:
			number = int(input("How many tables would you like to add: "))
			validInput = True
		except ValueError:
			validInput = False
			print("Invalid input")

	tablesFile = open("tables.txt","a")
	for x in range(0,number):

		validInput = False
		while (not validInput):
			try:
				newTable = input("Enter x and y value of coordinate of next table with a space inbetween: ")
				newTable = [float(i) for i in newTable.split(" ")]
				validInput = len(home)==2
			except ValueError:
				validInput=False
				print("Invalid input")

		tableList.append(newTable)
		tablesFile.write(str(newTable[0]) +" "+ str(newTable[1]) +"\n")
		print("Table has been saved and assigned table number "+str(len(tableList)))

	tablesFile.close()
	return tableList

def deliverTo():
	validInput = False
	while (not validInput):
		try:
			deliverTo = input("Enter what table to deliver to: ")
			deliverTo = int(deliverTo)
			if ((deliverTo<1) and (deliverTo>len(tableList))):
				validInput=False
				print("invalid input")
			else:
				validInput=True
		except ValueError:
			validInput=False
			print("invalid input")

	travelTo(tableList[deliverTo-1])

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
	home = []

	try:
		tablesFile = open("tables.txt","r+")
	except:
		tablesFile = open("tables.txt","w+")
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

	while (dontexit):
		try:
			print()
			print("Enter DEFINEHOME to define home location")
			print("Enter ADDTABLE to add new table")
			print("Enter DELIVERTO to deliver to a table")
			print("Enter RETURNHOME to return robot home")
			print("Enter MOVETABLE to change table location")
			print("Enter EXIT to exit")
			nextCommand = input()

			if (nextCommand == "DEFINEHOME"):
				home = defineHome()

			elif (nextCommand == "ADDTABLE"):
				tableList = addTables(tableList)

			elif (nextCommand == "MOVETABLE"):
				moveTable(tableList)

			elif (nextCommand == "DELIVERTO"):
				deliverTo()

			elif (nextCommand == "RETURNHOME"):
				if (not(home==[])):
					travelTo(home)
				else:
					print("Must define home first")

			elif (nextCommand == "EXIT"):
				dontexit=False

		except rospy.ROSInterruptException:
			rospy.loginfo("Ctrl-C caught. Quitting")
