from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup

import RPi.GPIO as GPIO

import rospy
import std_msgs
from std_msgs.msg import String

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def callback(msg):
	if msg.data == 'going home':
		print('going home')
		GPIO.output(18,GPIO.HIGH)
		#App.get_running_app().root.current = "returning"
	if msg.data  == 'going to table':
		print('going to table')
		GPIO.output(18,GPIO.HIGH)
		#App.get_running_app().root.current = "delivering"
	if msg.data == 'Reached home':
		GPIO.output(18,GPIO.LOW)
		App.get_running_app().root.current = "kitchen"
	if msg.data == 'Reached table':
		GPIO.output(18,GPIO.LOW)
		App.get_running_app().root.current = "table"
	if msg.data == 'Stuck':
		PIO.output(18,GPIO.LOW)
		App.get_running_app().root.current = "warn"
		
pub = rospy.Publisher('chatter', String, queue_size=10)
sub = rospy.Subscriber('navi_status', String, callback, queue_size = 10)

rospy.init_node('talker', anonymous=True)

#Define our different screens
class Kitchen(Screen):
	def table_pressed(self, instance):
		global tables
		if instance in tables:
			tables.remove(instance)
			# create content and add to the popup
			
		else:
			tables.append(instance)
			
	def confirm(self, instance):
		global tables
		if len(tables) == 1:
			tables[0].state = 'normal'
			self.manager.current = "delivering"
			pub.publish(str(tables[0].text.split(' ')[1]))
			tables = []
			GPIO.output(18, GPIO.HIGH)
		else:
			content = Button(text='Error: Only select one table.', font_size = 20, color = (1.0, 0.0, 0.0, 1.0), background_color = (0.0, 0.0, 0.0, 0.0))
			popup = Popup(title = 'Warning.', content=content, auto_dismiss=False, size_hint=(None, None), size=(500, 200))

			# bind the on_press event of the button to the dismiss function
			content.bind(on_press=popup.dismiss)

			# open the popup
			popup.open()
		

class Kitchen2(Screen):
	def table_pressed(self, instance):
		global tables
		if instance in tables:
			tables.remove(instance)
			# create content and add to the popup
			
		else:
			tables.append(instance)
			
	def confirm(self, instance):
		global tables
		if len(tables) == 1:
			tables[0].state = 'normal'
			self.manager.current = "delivering"
			pub.publish(str(tables[0].text.split(' ')[1]))
			tables = []
			GPIO.output(18,GPIO.HIGH)
		else:
			content = Button(text='Only select one table.')
			popup = Popup(title = 'Warning.', content=content, auto_dismiss=False, size_hint=(None, None), size=(500, 200))

			# bind the on_press event of the button to the dismiss function
			content.bind(on_press=popup.dismiss)

			# open the popup
			popup.open()



class Table(Screen):
	def returnHome(self, instance):
		self.manager.current = "returning"
		pub.publish('Recieved')
		GPIO.output(18,GPIO.HIGH)

class Delivering(Screen):
	def openDoor(self, instance):
		print('low')
		GPIO.output(18,GPIO.LOW)
		
class Returning(Screen):
	def openDoor(self, instance):
		print('low')
		GPIO.output(18,GPIO.LOW)

class Warn(Screen):
	def openDoor(self, instance):
		print('low')
		GPIO.output(18,GPIO.LOW)
	
class WindowManager(ScreenManager):
	pass

# Designate Our .kv design file 
kv = Builder.load_file('new_window.kv')


class AwesomeApp(App):
	def build(self):
		return kv
		
if __name__ == '__main__':
	print(4)
	global tables
	tables = []
	AwesomeApp().run()
