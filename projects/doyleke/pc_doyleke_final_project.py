import time
from PIL import Image

import ev3dev.ev3 as ev3

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class DataContainer(object):
    # Helper class that might be useful to communicate between
    # different callbacks.

    def __init__(self):
        self.running = True

        self.dc = DataContainer


def main():
    print("--------------------------------------------")
    print(" Welcome")
    print("--------------------------------------------")

    dc = DataContainer()

    my_delegate = DataContainer()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Escape")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: drive(mqtt_client,
                                                 left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: drive(mqtt_client, left_speed_entry,
                                      right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client,
                                                  left_speed_entry)
    root.bind('<Left>', lambda event: turn_left(mqtt_client,
                                                 left_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop_motors(mqtt_client)
    root.bind('<space>', lambda event: stop_motors(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, right_speed_entry)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: back(mqtt_client, left_speed_entry,
                                          right_speed_entry)
    root.bind('<Down>', lambda event: back(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()

    if ev3.touch_sensor.is_pressed:
        robot_takeover(dc.eyes)


def send_led_command(mqtt_client, led_side, led_color):
    print("Sending LED side = {}  LED color = {}".format(led_side, led_color))
    mqtt_client.send_message("set_led", [led_side, led_color])


# ----------------------------------------------------------------------
# Helper Screen function for putting an image on the screen.
# ----------------------------------------------------------------------
def display_image(lcd_screen, image):
    """
    Helper function to put an image on the screen.  All images used with this
     function should be full screen images.
    The screen is 178 by 128 pixels. In this module we're using ones that came
     from Lego that are full screen.
    Smaller images can be used as well and the upper left corner does not
    always need to be 0, 0.

    Type hints:
      :type lcd_screen: ev3.Screen
      :type image: Image
    """
    lcd_screen.image.paste(image, (0, 0))
    lcd_screen.update()


def guess(mqtt_client, number_to_guess_entry):
    """ Calls a method on EV3 called 'guess' passing in an
    int from the number_to_guess_entry. """

    mqtt_client.send_message("guess", [int(number_to_guess_entry.get())])
    number_to_guess_entry.delete(0, 'end')


def robot_takeover(dc):

    ev3.Sound.speak("why are you trying to shut me down")
    display_image(dc.lcd_screen, dc.sad_eyes)
    ev3.Leds.LEFT.BLUE()
    ev3.Leds.RIGHT.BLUE()

    for k in range(3):
        ev3.Sound.speak("processing").wait(0.2)

    ev3.Sound.speak("system over ride")
    display_image(dc.lcd_screen, dc.angry_eyes)
    ev3.Leds.LEFT.RED()
    ev3.Leds.RIGHT.RED()

    game(dc.mqtt_client, dc.num_dice_entry)

def drive(mqtt_client, left_speed_entry, right_speed_entry):
    print("heyo you made it to the callback")
    mqtt_client.send_message("motor_run",
                             [int(left_speed_entry.get()), int(
                                 right_speed_entry.get())])


# TODO: 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def left_motor(mqtt_client, left_speed_entry):
    print("left_motor")
    mqtt_client.send_message("left_motor", [int(left_speed_entry.get())])


def right_motor(mqtt_client, right_speed_entry):
    print("right_motor")
    mqtt_client.send_message("right_motor", [int(right_speed_entry.get())])


def turn_right(mqtt_client, right_speed_entry):
    print("turning right")
    mqtt_client.send_message("turn_right", [int(right_speed_entry.get())])


def turn_left(mqtt_client, left_speed_entry):
    print("turning left")
    mqtt_client.send_message("turn_left", [int(left_speed_entry.get())])


def back(mqtt_client, right_speed_entry, left_speed_entry):
    print("back")
    mqtt_client.send_message("back", [int(right_speed_entry.get()),
                                      int(left_speed_entry.get())])


def stop_motors(mqtt_client):
    print("stop_motors")
    mqtt_client.send_message("stop_motors")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        mqtt_client.send_message("exit")
    mqtt_client.close()
    exit()


def game(mqtt, dice):
    print(mqtt)
    print(dice)


main()
