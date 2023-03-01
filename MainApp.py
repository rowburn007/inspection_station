import os
import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

class TCApp(App):
    def build(self):
        # Define FloatLayout
        layout = FloatLayout()

        # Define Image Widget
        image = Image(source='next.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(image)

        # Define Button Widget
        button = Button(text="Start Classification", size_hint=(0.5, 0.1), pos_hint={'x':0.25, 'y':0.05})
        button.bind(on_press=self.run_script)
        layout.add_widget(button)

        return layout

    def run_script(self, instance):
        # Call Shell Script
        os.system('./run-tc.sh')

if __name__ == "__main__":
    TCApp().run()