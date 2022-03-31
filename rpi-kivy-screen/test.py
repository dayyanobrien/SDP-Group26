from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
		
#Define our different screens
class Kitchen(Screen):
	pass

class Kitchen2(Screen):
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
	AwesomeApp().run()
