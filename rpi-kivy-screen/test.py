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

import rospy
import std_msgs
from std_msgs.msg import String

pub = rospy.Publisher('chatter', String, queue_size=10)
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
			pub.publish(str(tables[0].text))
			tables = []
		else:
			content = Button(text='Only select one table.')
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
			pub.publish(str(tables[0].text))
			tables = []
		else:
			content = Button(text='Only select one table.')
			popup = Popup(title = 'Warning.', content=content, auto_dismiss=False, size_hint=(None, None), size=(500, 200))

			# bind the on_press event of the button to the dismiss function
			content.bind(on_press=popup.dismiss)

			# open the popup
			popup.open()
	
class Table(Screen):
	pass

class Delivering(Screen):
	pass

class Returning(Screen):
	pass

class Warn(Screen):
	pass

class WindowManager(ScreenManager):
	pass

# Designate Our .kv design file 
kv = Builder.load_file('new_window.kv')


class AwesomeApp(App):
	def build(self):
		return kv
		
if __name__ == '__main__':
	global tables
	tables = []
	AwesomeApp().run()
