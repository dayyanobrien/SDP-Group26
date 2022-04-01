import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
import time


def talker():
    #move_base = rospy.Subscriber("move_base/status", GoalStatusArray, callback, queue_size=10)
    pub = rospy.Publisher('navi_status',String, queue_size = 10)
    rospy.init_node('chatter', anonymous=True)
    #rospy.spin()
    while True:
        pub.publish('going to table')
        time.sleep(1)
        input('enter')
        pub.publish('Reached table')
        time.sleep(1)
        input('enter')
        pub.publish('going home')
        time.sleep(1)
        input('enter')
        pub.publish('Reached home')
        input('enter')
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass