
import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class Ev3delegate(object):
    def __init__(self):
        self.running = True

    def drive_shapes(self, sides, fill_color, outline_color):
        sdf


def main():
    my_delegate = Ev3delegate()

    mqtt_client = com.MqttClient(my_delegate)

    mqtt_client.connect_to_ev3()

    mqtt_client.connect_to_pc()


main()
