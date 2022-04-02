import rospy
import std_msgs
from std_msgs.msg import String
global data

pub = rospy.Publisher('chatter', String, queue_size=10)
sub = rospy.Subscriber('navi_status', String, callback, queue_size = 10)
rospy.init_node('talker', anonymous=True)



numberofDeliveries = 0
cycles = 0
pub.publish("Recieved")
while (data!=stuck):
    cycle++
    print(j)
    for i in range(1,16):
        numberofDeliveries++
        print(numberofDeliveries)
        pub.publish(str(i))
        while (data!="Reached table")
        pub.publish("Recieved")
        while (data!='Reached home')

print("Number of deliveries before failure")
print(numberofDeliveries)
print("Number of cycles before failure")
print(numberofDeliveries)

def callback(msg):
    data = msg.data
    """
	if msg.data == 'going home':
		print('going home')
		#App.get_running_app().root.current = "returning"
	if msg.data  == 'going to table':
		print('going to table')
		#App.get_running_app().root.current = "delivering"
	if msg.data == 'Reached home':
		App.get_running_app().root.current = "kitchen"
	if msg.data == 'Reached table':
		App.get_running_app().root.current = "table"
	if msg.data == 'Stuck':
		App.get_running_app().root.current = "warn"
    """
