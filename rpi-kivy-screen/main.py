import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import RPi.GPIO as GPIO

import rospy
import std_msgs

rospy.init_node('main')
pub = rospy.Publisher('table_state', int, queue_size = 10) #problem



#for now, use a global for blink speed (better implementation TBD):
speed = 1.0

# Set up GPIO:
tablePin = 18 #PIN for read table
orderRecievePin = 25 
confirmPin = 27


buttonPin = 22
flashLedPin = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(tablePin, GPIO.OUT)
GPIO.output(tablePin, GPIO.LOW)
GPIO.setup(confirmPin, GPIO.OUT)
GPIO.output(confirmPin, GPIO.LOW)
GPIO.setup(flashLedPin, GPIO.OUT)
GPIO.output(flashLedPin, GPIO.LOW)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define some helper functions:

# This callback will be bound TO CONFIRM AND TABLE BUTTON:
#TO DO: PUBLISH TABLE NUMBER


def press_callback(obj):
	global TABLE_NUMBER
	global table_obj
	print("Button pressed,", obj.text)
	if obj.text == 'Received':
		print("Received")
		pub.publish('Recieved')
	if obj.text == 'Table 1':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 1
		else:
			TABLE_NUMBER = 0
	if obj.text == 'Table 2':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 2
		else:
			TABLE_NUMBER = 0
	if obj.text == 'Table 3':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 3
		else:
			TABLE_NUMBER = 0
	if obj.text == 'Table 4':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 4
		else:
			TABLE_NUMBER = 0
	if obj.text == 'Table 5':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 5
		else:
			TABLE_NUMBER = 0
	if obj.text == 'Table 6':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 6
		else:
			TABLE_NUMBER = 0
	if obj.text == 'Table 7':
		if obj.state == "down":
			if TABLE_NUMBER == 0:
				table_obj = obj
				TABLE_NUMBER = 7
		else:
			TABLE_NUMBER = 0
			
	if obj.text == 'Confirm table':
		if TABLE_NUMBER != 0:
			table_obj.state = "normal"
			print("Table",TABLE_NUMBER,"confirmed!")
			TABLE_NUMBER = 0
			pub.publish(TABLE_NUMBER)
		else:
			print("No table selected, or multiple buttons. Retry")




def buzzer_off(dt):
	GPIO.output(tablePin, GPIO.LOW)

# Toggle the flashing LED according to the speed global
# This will need better implementation
def flash(dt):
	global speed
	GPIO.output(flashLedPin, not GPIO.input(flashLedPin))
	Clock.schedule_once(flash, 1.0/speed)

# This is called when the slider is updated:
def update_speed(obj, value):
	global speed
	print("Updating speed to:" + str(obj.value))
	speed = obj.value

# Modify the Button Class to update according to GPIO input:
class InputButton(Button):
	def update(self, dt):
		if GPIO.input(buttonPin) == True:
			self.state = 'normal'
		else:
			self.state = 'down'			

class MyApp(App):

	def build(self):
		# Set up the layout:
		layout = GridLayout(cols=5, spacing=30, padding=30, row_default_height=150)

		# Make the background gray:
		with layout.canvas.before:
			Color(.2,.2,.2,1)
			self.rect = Rectangle(size=(800,600), pos=layout.pos)

		# Schedule the update of the state of the GPIO input button:
		# Create the rest of the UI objects (and bind them to callbacks, if necessary):
		table1Control = ToggleButton(text="Table 1")
		table1Control.bind(on_press=press_callback)
		table2Control = ToggleButton(text="Table 2")
		table2Control.bind(on_press=press_callback)
		table3Control = ToggleButton(text="Table 3")
		table3Control.bind(on_press=press_callback)
		table4Control = ToggleButton(text="Table 4")
		table4Control.bind(on_press=press_callback)
		table5Control = ToggleButton(text="Table 5")
		table5Control.bind(on_press=press_callback)
		table6Control = ToggleButton(text="Table 6")
		table6Control.bind(on_press=press_callback)
		table7Control = ToggleButton(text="Table 7")
		table7Control.bind(on_press=press_callback)
		outputControl = Button(text="Confirm table")
		outputControl.bind(on_press=press_callback)
		beepButton = Button(text="Received")
		beepButton.bind(on_press=press_callback)
		wimg = Image(source='logo.png')
		# Add the UI elements to the layout:
		layout.add_widget(wimg)
		layout.add_widget(table1Control)
		layout.add_widget(table2Control)
		layout.add_widget(table3Control)
		layout.add_widget(table4Control)
		layout.add_widget(table5Control)
		layout.add_widget(table6Control)
		layout.add_widget(table7Control)
		layout.add_widget(outputControl)
		layout.add_widget(beepButton)

		# Start flashing the LED
		Clock.schedule_once(flash, 1.0/speed)
		return layout

if __name__ == '__main__':
	global TABLE_NUMBER
	TABLE_NUMBER = 0 
	global table_obj
	table_obj = 0
	MyApp().run()
