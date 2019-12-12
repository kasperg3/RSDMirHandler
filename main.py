import requests

import kivy

from kivy.app import App
from kivy.uix.button import Button
#Probable will change after network is ready
url = 'http://10.10.19.40/api/v2.0.0/'

Authorization = {
    'Authorization': "PUT_THE_RIGHT_KEY"}
language = {'Accept-Language': "en_US"}


class RestMiR():
    def __init__(self):
        self.authorization = {
            'Authorization': "Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=="}
        self.HOST = 'http://10.10.19.40/api/v2.0.0/'

    #In the mission we will have to set coils (plc registers) in order to get information if robot has docked and etc.
    def read_register(self, register_id):
        try:
            response = requests.get(url + 'registers/' + str(register_id), headers=self.authorization)
        except requests.exceptions.ConnectionError:
            return

        register_value = 0
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)

        if (response.json()['id'] == register_id):
            register_value = response.json()['value']
        return register_value


    #As above, we can set the register when loading on the robot is ready to move to main table
    def write_register(self, register_id, value):
        data = {"value": value}
        response = requests.put(url + 'registers/' + str(register_id), json = data, headers=self.authorization)
        if response.status_code != 200:
            print(response.status_code)
        return 0

# class in which we are creating the button
class ButtonApp(App):
    mir = RestMiR()
    def build(self):
        btn = Button(text="Release MIR",
                     font_size="50sp",
                     background_color=(1, 1, 1, 1),
                     color=(1, 1, 1, 1))

        # bind() use to bind the button to function callback
        btn.bind(on_release=self.callback)
        return btn

    def callback(self, event):
        #Release the mir
        #value = self.mir.read_register(150)
        #self.mir.write_register(150, not value)
        self.mir.write_register(150, 1)
        print("Register 150 Value: " + str(self.mir.read_register(150)))


root = ButtonApp()
root.run()
