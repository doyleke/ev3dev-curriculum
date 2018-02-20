# import mqtt_remote_method_calls as com
# import robot_controller_mine as robo
# import ev3dev as ev3

import ev3dev.ev3 as ev3
import time
import random
from PIL import Image
import mqtt_remote_method_calls as com

# def main():
#     robot = robo.Snatch3r()
#     mqtt_client = com.MqttClient(robot)
#     mqtt_client.connect_to_pc()
#     # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
#     robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


class GameMaster(object):
    """ Delegate that listens for responses from EV3. """

    def __init__(self):
        self.mqtt_client = None
        self.lcd = ev3.Screen()
        self.ir_sensor = ev3.InfraredSensor()
        self.running = False

    def get_distance(self):
        distance = self.ir_sensor.proximity

        self.mqtt_client.send_message["guess_response",
                                      distance]

    def loop_forever(self):
        btn = ev3.Button()
        self.running = True
        while not btn.backspace and self.running:
            # Do nothing while waiting for commands
            time.sleep(0.01)
        self.mqtt_client.close()
        # Copied from robot.shutdown
        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)


def main():
    print("Ready")
    my_delegate = GameMaster()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus use EV3 as broker.
    my_delegate.loop_forever()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


main()