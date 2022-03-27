# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
import os
import tf
import sys
from std_msgs.msg import String
#from std_msgs import range
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
			# send open door signal!!!!!!!!!

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
			newTable.append(0.0)
		elif direction == 'D':
			newTable.append(3.1)
		elif direction == 'L':
			newTable.append(1.65)
		elif direction == 'R':
			newTable.append(-1.65)

		tablesFile.write(str(newTable[0]) +" "+ str(newTable[1]) + " " + str(newTable[2]) + "\n")
		#tablesFile.write(str(newTable[0]) + " " + str(newTable[1]) +"\n")
		print("Table has been saved and assigned table number "+str(len(tableList)))
	tablesFile.close()
	return tableList

def deliverTo():
	deliverTo = input("Enter what table to deliver to: ")
	deliverTo = int(deliverTo)-1
	
	travelTo(tableList[deliverTo])
	input("Press enter to return")
	travelTo(home)

def travelTo(location):
	#############
	#rospy.init_node('nav_test', anonymous=False)
	navigator = Navigation()
	print(location)
	# Customize the following values so they are appropriate for your location
	position = {'x': location[0], 'y' : location[1]}
	#quaternion = {'r1' : location[2], 'r2' : location[3], 'r3' : location[4], 'r4' : location[5]}
	#quaternion = {'r1' : 0.7, 'r2' : 0, 'r3' : 0, 'r4' : -0.7}
	#L: 1.65   R: -1.65   Up: 0.0    down: 3.1
	quat = tf.transformations.quaternion_from_euler(0, 0, location[2])
	quaternion = {'r1' : quat[0], 'r2' : quat[1], 'r3' : quat[2], 'r4' : quat[3]}

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

def tableNumber_callback(data):
	tableNumber = data.data
	print(tableNumber)
	if tableNumber.isnumeric():
		if int(tableNumber) > 0:
			tableNumber = int(tableNumber)
			print(tableList[tableNumber])
			travelTo(tableList[tableNumber])
	if tableNumber == "Recieved":
		tableNumber = tableNumber
		print()
		travelTo(home)
	rospy.loginfo("tableNumber heard %s",data.data)
	rospy.sleep(1)

#def ultrasonic_callback(data):
#	distance = data.Float64
#	rospy.loginfo("Callback2 heard %s",data.data) 

def listener():
	#change table_state to chatter since thats on GUI
	rospy.Subscriber("chatter", String, tableNumber_callback)
	rospy.init_node('python_navi')
	#rospy.Subscriber("ultrasonic", Float64, ultrasonic_callback)
	# spin() simply keeps python from exiting until this node is stopped
	print('dasdasfxz')
	rospy.spin()

####################################################################################################################################
####################################################################################################################################
###########################################  MAIN  ##################################################################################

if __name__ == '__main__':
 
	dontexit = True
	tableList = []
	global home
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
		tableNumber = 0
		listener()
		print('sadsafd')
		try:
			print()
			print("Enter [1] DEFINEHOME to define home location")
			print("Enter [2] ADDTABLE to add new table")
			print("Enter [3] DELIVERTO to deliver to a table")
			print("Enter [4] RETURNHOME to return robot home")
			print("Enter [5] MOVETABLE to change table location")
			print("Enter [6] EXIT to exit")
			nextCommand = input()

			if (nextCommand == "1"):
				home = defineHome()

			elif (nextCommand == "2"):
				tableList = addTables(tableList)

			elif (nextCommand == "3"):
				deliverTo()

			elif (nextCommand == "4"):
				travelTo(home)

			elif (nextCommand == "5"):
				moveTable(tableList)

			elif (nextCommand == "6"):
				dontexit=False

		except rospy.ROSInterruptException:
			rospy.loginfo("Ctrl-C caught. Quitting")

