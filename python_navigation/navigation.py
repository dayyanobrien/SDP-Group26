# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
import os
import tf
import sys
from std_msgs.msg import String
from std_msgs.msg import Empty
#from std_msgs import range
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from geometry_msgs.msg import PoseWithCovarianceStamped
import time
import std_srvs.srv
from nav_msgs.msg import Odometry

velocity = 0.0
angular_vel = 0.0

class Navigation():
	def __init__(self):
		self.goal_sent = False

		# What to do if shut down (e.g. Ctrl-C or failure)
		rospy.on_shutdown(self.shutdown)

		# Tell the action client that we want to spin a thread by default
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		self.pub = rospy.Publisher('navi_status',String, queue_size=10)
		rospy.Subscriber("/odom", Odometry, odom_callback)
		
		rospy.loginfo("Wait for the action server to come up")

		# Allow up to 5 seconds for the action server to come up
		self.move_base.wait_for_server(rospy.Duration(5))

		self.stopped = False

	

	def goto(self, pos, quat):
		global velocity
		global angular_vel
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
		#success = self.move_base.wait_for_result(rospy.Duration(120))

		state = self.move_base.get_state()
		result = False

		timer = time.time()
		timer_clear = time.time()
		#timer_resend = time.time()
		self.stopped = False
		while not (state == GoalStatus.SUCCEEDED) and (time.time() - timer) <= 180 and (not self.stopped):
			# Start moving
			if (time.time() - timer_clear >= 5.5) and (abs(velocity) <= 0.03) and (angular_vel <= 0.03):
				print(velocity)
				print('cleaning!!!')
				clear_map = rospy.ServiceProxy('/move_base/clear_costmaps', std_srvs.srv.Empty())()
				timer_clear = time.time()
				print('resending!!!')
				self.move_base.send_goal(goal)
				timer_resend = time.time()
				print(state)
			# if (time.time() - timer_resend >= 4) and (abs(velocity) <= 0.01):
			# 	print('resending!!!')
			# 	self.move_base.send_goal(goal)
			# 	timer_resend = time.time()
			# 	print(state)
			time.sleep(1)
			state = self.move_base.get_state()
		if self.stopped:
			self.move_base.cancel_goal()
          #ometry_ms.SUCCEEDED:
		if state == GoalStatus.SUCCEEDED:
			# We made it!
			# send open door signal!!!!!!!!!

			result = True
		else:
			self.move_base.cancel_goal()

		self.goal_sent = False
		return result

	# def stop(self): 
	# 	self.stopped = True
	# 	print('in stop')
	# 	rospy.Subscriber("acml", PoseWithCovarianceStamped, callback)
	# 	#rospy.init_node('python_navi')

	def shutdown(self):
		self.stopped = True
		if self.goal_sent:
			self.move_base.cancel_goal()
		rospy.loginfo("Stop")
		rospy.sleep(1)

	def publish_status(self, state):
		self.pub.publish(state)

	

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

# def callback(msg):
# 	print('in callback')
# 	orientation_q = msg.pose.pose.orientation
# 	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
# 	(roll, pitch, yaw) = tf.transformations.euler_from_quaternion (orientation_list)
# 	curr_pos = msg.pose.pose
# 	location = [curr_pos.position.x, curr_pos.position.y,yaw]
# 	travelTo(location)

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
	
	travelTo(tableList[deliverTo],'Table')
	# opendoor
	input("Press enter to return")
	travelTo(home,'Home')
	# opendoor
	

def travelTo(location, des):
	#############
	#rospy.init_node('nav_test', anonymous=False)
	navigator = Navigation()
	#rospy.Service('/move_base/clear_costmaps', "{}")
	if des == 'Home':
		navigator.publish_status('going home')
	else:
		navigator.publish_status('going to table')
	

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
		if des == 'Home':
			navigator.publish_status('Reached home')
		else:
			navigator.publish_status('Reached table')
		rospy.loginfo("Hooray, reached the desired pose")
	else:
		navigator.publish_status('Stuck')

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
			#CLEAR MAP HERE
			clear_map = rospy.ServiceProxy('/move_base/clear_costmaps', std_srvs.srv.Empty())()
			travelTo(tableList[tableNumber],'Table')
			#CLEAR MAP HERE
			clear_map = rospy.ServiceProxy('/move_base/clear_costmaps', std_srvs.srv.Empty())()
	if tableNumber == "Recieved":
		tableNumber = tableNumber
		print()
		#CLEAR MAP HERE
		clear_map = rospy.ServiceProxy('/move_base/clear_costmaps', std_srvs.srv.Empty())()
		travelTo(home,'Home')
		#CLEAR MAP HERE
		clear_map = rospy.ServiceProxy('/move_base/clear_costmaps', std_srvs.srv.Empty())()
	rospy.loginfo("tableNumber heard %s",data.data)
	rospy.sleep(1)

#def ultrasonic_callback(data):
#	distance = data.Float64
#	rospy.loginfo("Callback2 heard %s",data.data) 

def odom_callback(msg):
	global velocity
	global angular_vel
	velocity = msg.twist.twist.linear.x
	angular_vel = msg.twist.twist.angular.x + msg.twist.twist.angular.y + msg.twist.twist.angular.z


def listener():
	#change table_state to chatter since thats on GUI
	rospy.Subscriber("chatter", String, tableNumber_callback)
	rospy.init_node('python_navi')
	
	#rospy.Service.call("/move_base/clear_costmaps", "{}")
	#rospy.Subscriber("ultrasonic", Float64, ultrasonic_callback)
	# spin() simply keeps python from exiting until this node is stopped
	#print('dasdasfxz')
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
				travelTo(home,'Home')

			elif (nextCommand == "5"):
				moveTable(tableList)

			elif (nextCommand == "6"):
				dontexit=False

		except rospy.ROSInterruptException:
			rospy.loginfo("Ctrl-C caught. Quitting")

