import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color

class HelloWorld(App):
    def build(self):
      return BoxLayout()

helloWorld = HelloWorld()
helloWorld.run()
