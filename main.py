import requests

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class RestMiR():
    def __init__(self):
        # Probable will change after network is ready
        self.url = 'http://10.10.19.40/api/v2.0.0/'
        language = {'Accept-Language': "en_US"}
        self.authorization = {'Authorization': "Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=="}
        self.HOST = 'http://10.10.19.40/api/v2.0.0/'

    def read_register(self, register_id):
        try:
            response = requests.get(self.url + 'registers/' + str(register_id), headers=self.authorization)
        except requests.exceptions.ConnectionError:
            return

        register_value = 0

        if (response.json()['id'] == register_id):
            register_value = response.json()['value']
        return register_value

    def write_register(self, register_id, value):
        data = {"value": value}
        try:
            requests.put(self.url + 'registers/' + str(register_id), json = data, headers=self.authorization)
        except requests.exceptions.ConnectionError:
            return
        return

# class in which we are creating the button
class ButtonApp(App):
    mir = RestMiR()
    def build(self):
        self.btn = Button(text="Release MIR",
                          font_size="50sp",
                          background_color=(1, 1, 1, 1),
                          color=(1, 1, 1, 1), size_hint=(1,1))

        self.btn2 = Button(text="Register 150 Value: ",
                           font_size="20sp",
                           background_color=(1, 1, 1, 1),
                           color=(1, 1, 1, 1), size_hint=(0.5,1))

        self.btn3 = Button(text="Charging: ",
                           font_size="20sp",
                           background_color=(1, 1, 1, 1),
                           color=(1, 1, 1, 1), size_hint=(0.5,1))

        # bind() use to bind the button to function callback
        self.btn.bind(on_release=self.callback)
        self.btn2.bind(on_release=self.callback2)
        self.btn3.bind(on_release=self.callback3)
        self.layout1 = BoxLayout(orientation='horizontal', size_hint=(1,0.2))
        self.layout1.add_widget(self.btn2)
        self.layout1.add_widget(self.btn3)
        layout = BoxLayout(orientation='vertical', size_hint=(1,1))
        layout.add_widget(self.btn)
        layout.add_widget(self.layout1)

        return layout

    def callback(self, event):
        self.mir.write_register(150, 1)

    def callback2(self, event):
        self.btn2.text = "Register 150 Value: " + str(self.mir.read_register(150))

    def callback3(self, event):
        if self.mir.read_register(110) == 0:
            self.btn3.text = "Charging: False"
        else:
            self.btn3.text = "Charging: True"


root = ButtonApp()
root.run()
