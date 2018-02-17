
import tkinter
from tkinter import ttk
import time
import ev3dev.ev3 as ev3

import mqtt_remote_method_calls as com


class Ev3delegate(object):

    def __init__(self):
        self.running = True
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.ir_sensor.connected
        assert self.pixy

    def drive_shapes(self, sides, fill_color, outline_color):
        sdf

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)


def main():
    robot = Ev3delegate()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


main()
