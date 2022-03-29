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
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.submit = Button(text='Order', font_size=40)
        self.add_widget(self.submit)
        self.submit.bind(on_press=self.pressed)

    def pressed(self, instance):
        pressing = Secondtab()
        pressing()
        myapp.screen_manager.transition = SlideTransition(direction='left', duration=.25)    #You can change transition speed or you could just remove it to set it on default
        myapp.screen_manager.current = 'Secondtab'

class MyApp(App):

    def build(self):
        return LoginScreen()

        self.screen_manager = ScreenManager()

        self.loginscreen = LoginScreen()
        screen = Screen(name='LoginScreen')
        screen.add_widget(self.loginscreen)
        self.screen_manager.add_widget(screen)

        self.secondtab = Secondtab()
        screen = Screen(name='Secondtab')
        screen.add_widget(self.secondtab)
        self.screen_manager.add_widget(screen)

        return self.screen_manager
