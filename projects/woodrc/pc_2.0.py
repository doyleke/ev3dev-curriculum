#!/usr/bin/env python3
" This ifle is the "

import tkinter
from tkinter import ttk
# import ev3dev.ev3 as ev3
#import robot_controller_mine as robo
import time
import mqtt_remote_method_calls as com
import math


class MyDelegate(object):

# Done: 3. Create a method named guess_response within MyDelegate.
# guess_response needs to receive self and a string, feel free to call the string parameter message_from_ev3
# within the body of the method print message_from_ev3.  That's it.  You simply need to hear what EV3 tells you.
    def lookaround(self, distance):
        current_distance = distance
        print(current_distance)
        if math.fabs(current_distance) < 10:
            print("Too close!")
            # slide(self, 'Back')
            time.sleep(.05)


def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to
    # receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).

    pc_delegate = MyDelegate()
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    notebook = ttk.Notebook(root)

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    notebook.add(main_frame, text="Main Controls")
    notebook.grid()

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

    # TODO: 3. Implement the callbacks for the drive buttons. Set both the click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.

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
    left_button['command'] = lambda: turn_left(mqtt_client, left_speed_entry)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, left_speed_entry))

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

    dance_button = ttk.Button(main_frame, text="Dance Moves")
    dance_button.grid(row=0, column=1)
    dance_button['command'] = (lambda: dance_gui(mqtt_client, notebook, root))

    # btn = ev3.Button()
    # rc1.on_red_up = lambda state: forward_left_motor(state, robot)
    # rc1.on_red_down = lambda state: back_left_motor(state, robot)
    # rc1.on_blue_up = lambda state: forward_right_motor(state, robot)
    # rc1.on_blue_down = lambda state: back_right_motor(state, robot)
    # ev3.on_backspace = lambda state: handle_shutdown(state, dc)
    #
    # rc2.on_red_up = lambda state: handle_arm_up_button(state, robot)
    # rc2.on_red_down = lambda state: handle_arm_down_button(state, robot)
    # rc2.on_blue_up = lambda state: handle_calibrate_button(state, robot)
    # rc2.on_blue_down = lambda state: handle_shutdown(state, dc)

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# TODO: 4. Implement the functions for the drive button callbacks.
def drive(mqtt_client, left_speed_entry, right_speed_entry):
    # print("heyo you made it to the callback")
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


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def dance_gui(mqtt_client, notebook, root):
    print("Dace Moves")
    nb = notebook

    dance_frame = ttk.Frame(root, padding=20, relief='raised')
    dance_frame.grid()
    nb.add(dance_frame, text="Dance Moves")
    nb.grid()

    clap_button = ttk.Button(dance_frame, text="Clap")
    clap_button.grid(row=0, column=1)
    clap_button['command'] = (lambda: clap(mqtt_client))

    slide_buttonR = ttk.Button(dance_frame, text="Slide")
    slide_buttonR.grid(row=1, column=2)
    slide_buttonR['command'] = (lambda: slide(mqtt_client, 'Right'))

    slide_buttonL = ttk.Button(dance_frame, text="Slide")
    slide_buttonL.grid(row=1, column=0)
    slide_buttonL['command'] = (lambda: slide(mqtt_client, 'Left'))

    stomp_buttonL = ttk.Button(dance_frame, text="Stomp")
    stomp_buttonL.grid(row=2, column=0)
    stomp_buttonL['command'] = (lambda: stomp(mqtt_client, 'Left'))

    stomp_buttonR = ttk.Button(dance_frame, text="Stomp")
    stomp_buttonR.grid(row=2, column=2)
    stomp_buttonR['command'] = (lambda: stomp(mqtt_client, 'Right'))

    chacha_button = ttk.Button(dance_frame, text="ChaCha")
    chacha_button.grid(row=3, column=1)
    chacha_button['command'] = (lambda: chacha(mqtt_client))

    small_slide_buttonL = ttk.Button(dance_frame, text="SmallSlide")
    small_slide_buttonL.grid(row=4, column=0)
    small_slide_buttonL['command'] = (lambda: small_slide(mqtt_client, 'Left'))

    small_slide_buttonR = ttk.Button(dance_frame, text="SmallSlide")
    small_slide_buttonR.grid(row=4, column=2)
    small_slide_buttonR['command'] = (lambda: small_slide(mqtt_client,
                                                          'Right'))

    crisscross_button = ttk.Button(dance_frame, text="Criss Cross")
    crisscross_button.grid(row=5, column=1)
    crisscross_button['command'] = (lambda: crisscross(mqtt_client))

    reverse_button = ttk.Button(dance_frame, text="Reverse")
    reverse_button.grid(row=6, column=1)
    reverse_button['command'] = (lambda: reverse(mqtt_client))

    charlie_brown_button = ttk.Button(dance_frame, text="Charlie Brown")
    charlie_brown_button.grid(row=7, column=1)
    charlie_brown_button['command'] = (lambda: charlie_brown(mqtt_client))

    charlie_brown_button = ttk.Button(dance_frame, text="Charlie Brown")
    charlie_brown_button.grid(row=7, column=1)
    charlie_brown_button['command'] = (lambda: charlie_brown(mqtt_client))

    hop_button = ttk.Button(dance_frame, text="Hop")
    hop_button.grid(row=8, column=1)
    hop_button['command'] = (lambda: stomp(mqtt_client, 'Hop'))

    dance_button = ttk.Button(dance_frame, text="Dance")
    dance_button.grid(row=9, column=1)
    dance_button['command'] = (lambda: dance(mqtt_client))

    dance_button2 = ttk.Button(dance_frame, text="Dance 2")
    dance_button2.grid(row=10, column=1)
    dance_button2['command'] = (lambda: dancetwo(mqtt_client))


def clap(mqtt_client):
    looking(mqtt_client)
    # mqtt_client.send_message("arm_up")
    # mqtt_client.send_message("arm_down")
    print("Clap")


def slide(mqtt_client, direction):
    looking(mqtt_client)
    if direction == 'Left':
        print('Slide to the ' + direction)
        mqtt_client.send_message("turn_degrees", [90, 900])
        mqtt_client.send_message("drive_inches", [4, 900])
        mqtt_client.send_message("turn_degrees", [-90, 900])
    elif direction == 'Right':
        print('Slide to the ' + direction)
        mqtt_client.send_message("turn_degrees", [90, 900])
        mqtt_client.send_message("drive_inches", [-4, 500])
        mqtt_client.send_message("turn_degrees", [-90, 900])
    elif direction == 'Back':
        print('Tack it back now, Yall!')
        mqtt_client.send_message("drive_inches", [-6, 500])
        time.sleep(3)
    else:
        print('Error!')


def stomp(mqtt_client, direction):
    looking(mqtt_client)

    if direction == 'Left':
        print(direction + "foot. Lets stomp")
        mqtt_client.send_message("turn_degrees", [-20, 300])
        mqtt_client.send_message("turn_degrees", [20, 300])
    elif direction == 'Right':
        print(direction + "foot. Lets stomp")
        mqtt_client.send_message("turn_degrees", [20, 300])
        mqtt_client.send_message("turn_degrees", [-20, 300])
    elif direction == 'Hop':

        print('Hop')
        mqtt_client.send_message("drive_inches", [1, 500])
        mqtt_client.send_message("drive_inches", [-1, 500])
        time.sleep(2)
    else:
        print('Error!')


def chacha(mqtt_client):
    looking(mqtt_client)
    print("Chacha real smooth!")
    mqtt_client.send_message("drive_inches", [2.5, 500])
    mqtt_client.send_message("turn_degrees", [10, 900])
    mqtt_client.send_message("turn_degrees", [-20, 900])
    mqtt_client.send_message("drive_inches", [-2.5, 500])
    mqtt_client.send_message("turn_degrees", [20, 900])
    mqtt_client.send_message("turn_degrees", [-10, 900])
    mqtt_client.send_message("drive_inches", [2.5, 500])
    mqtt_client.send_message("turn_degrees", [10, 900])
    mqtt_client.send_message("turn_degrees", [-20, 900])
    mqtt_client.send_message("drive_inches", [-2.5, 500])
    mqtt_client.send_message("turn_degrees", [20, 900])
    mqtt_client.send_message("turn_degrees", [-10, 900])
    print("Complete")


def small_slide(mqtt_client, direction):
    looking(mqtt_client)
    if direction == 'Left':
        print('To the ' + direction)
        mqtt_client.send_message("turn_degrees", [90, 900])
        mqtt_client.send_message("drive_inches", [2, 500])
        mqtt_client.send_message("turn_degrees", [-90, 900])
        time.sleep(1.5)

    elif direction == 'Right':
        print('To the ' + direction)
        mqtt_client.send_message("turn_degrees", [-90, 900])
        mqtt_client.send_message("drive_inches", [2, 500])
        mqtt_client.send_message("turn_degrees", [90, 900])
        time.sleep(1.5)
    else:
        print('Error!')


def crisscross(mqtt_client):
    looking(mqtt_client)
    print("Criss-Cross!")
    mqtt_client.send_message("turn_degrees", [15, 900])
    mqtt_client.send_message("turn_degrees", [-30, 900])
    mqtt_client.send_message("turn_degrees", [15, 900])
    time.sleep(.5)


def reverse(mqtt_client):
    looking(mqtt_client)
    print("Reverse! (Reverse!)")
    mqtt_client.send_message("turn_degrees", [30, 900])
    mqtt_client.send_message("turn_degrees", [-60, 900])
    mqtt_client.send_message("turn_degrees", [30, 900])
    time.sleep(.2)


def charlie_brown(mqtt_client):
    looking(mqtt_client)
    print("Charlie Brown")
    mqtt_client.send_message("drive_inches", [2.5, 500])
    mqtt_client.send_message("drive_inches", [-2.5, 500])
    mqtt_client.send_message("drive_inches", [2.5, 500])
    mqtt_client.send_message("drive_inches", [-2.5, 500])
    mqtt_client.send_message("drive_inches", [2.5, 500])
    mqtt_client.send_message("drive_inches", [-2.5, 500])
    time.sleep(.5)


def looking(mqtt_client):
    mqtt_client.send_message("get_distance")
    mqtt_client.send_message("get_distance")
    mqtt_client.send_message("get_distance")
    mqtt_client.send_message("get_distance")
    mqtt_client.send_message("get_distance")


def dance(mqtt_client):
    mqtt_client.send_message("play_song")
    time.sleep(.05)
    small_slide(mqtt_client, 'Left')
    slide(mqtt_client, 'Back')
    stomp(mqtt_client, 'Hop')
    stomp(mqtt_client, 'Hop')
    reverse(mqtt_client)
    reverse(mqtt_client)
    slide(mqtt_client, 'Left')
    slide(mqtt_client, 'Right')
    reverse(mqtt_client)
    reverse(mqtt_client)
    chacha(mqtt_client)
    chacha(mqtt_client)
    time.sleep(10)
    # small_slide(mqtt_client, 'Left')
    # slide(mqtt_client, 'Back')
    # stomp(mqtt_client, 'Hop')
    # stomp(mqtt_client, 'Hop')
    # stomp(mqtt_client, 'Hop')
    # stomp(mqtt_client, 'Hop')
    # stomp(mqtt_client, 'Right')
    # stomp(mqtt_client, 'Left')
    # charlie_brown(mqtt_client)
    # slide(mqtt_client, 'Right')
    # slide(mqtt_client, 'Left')
    # slide(mqtt_client, 'Back')
    # chacha(mqtt_client)


def dancetwo(mqtt_client):
    # mqtt_client.send_message("play_song")
    time.sleep(.05)
    slide(mqtt_client, 'Back')
    stomp(mqtt_client, 'Hop')
    stomp(mqtt_client, 'Hop')
    chacha(mqtt_client)
    chacha(mqtt_client)
    time.sleep(10)
















# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()