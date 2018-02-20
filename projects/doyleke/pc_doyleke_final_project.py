import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to
    # receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("TIME IS RUNNING OUT")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    red_unscramble = ttk.Label(main_frame, text="dre")
    red_unscramble.grid(row=0, column=0)
    r_unscrambled = ttk.Entry(main_frame, width=8)
    r_unscrambled.insert(0, "Guess")
    r_unscrambled.grid(row=1, column=0)

    orange_unscramble = ttk.Label(main_frame, text="regnao")
    orange_unscramble.grid(row=0, column=1)
    o_unscrambled = ttk.Entry(main_frame, width=8)
    o_unscrambled.insert(0, "Guess")
    o_unscrambled.grid(row=1, column=1)

    yellow_unscramble = ttk.Label(main_frame, text="wlely")
    yellow_unscramble.grid(row=0, column=2)
    y_unscrambled = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    y_unscrambled.insert(0, "Guess")
    y_unscrambled.grid(row=1, column=2)

    green_unscramble = ttk.Label(main_frame, text="reneg")
    green_unscramble.grid(row=2, column=0)
    g_unscrambled = ttk.Entry(main_frame, width=8)
    g_unscrambled.insert(0, "Guess")
    g_unscrambled.grid(row=3, column=0)

    blue_unscramble = ttk.Label(main_frame, text="elub")
    blue_unscramble.grid(row=2, column=1)
    b_unscrambled = ttk.Entry(main_frame, width=8)
    b_unscrambled.insert(0, "Guess")
    b_unscrambled.grid(row=3, column=1)

    purple_unscramble = ttk.Label(main_frame, text="leuprp")
    purple_unscramble.grid(row=2, column=2)
    p_unscrambled = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    p_unscrambled.insert(0, "Guess")
    p_unscrambled.grid(row=3, column=2)


    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Check")
    q_button.grid(row=5, column=0)
    q_button['command'] = (lambda: game_guess(mqtt_client, red_unscramble,
                                              o_unscrambled, y_unscrambled,
                                              g_unscrambled, b_unscrambled, p_unscrambled))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=5, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, False))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------


def game_guess(mqtt_client, r_unscrambled, o_unscrambled, y_unscrambled,
               g_unscrambled, b_unscrambled, p_unscrambled):
    if r_unscrambled == 'red':
        mqtt_client.send_message("leds_red")
        mqtt_client.send_message("left_motor", '600')
        mqtt_client.send_message("stop_motors")
    if o_unscrambled == 'orange':
        mqtt_client.send_message("leds_orange")
        mqtt_client.send_message("right_motor", '600')
        mqtt_client.send_message("stop_motors")
    if y_unscrambled == 'yellow':
        mqtt_client.send_message("leds_yellow")
        mqtt_client.send_message("left_motor", '600')
        mqtt_client.send_message("stop_motors")
    if g_unscrambled == 'green':
        mqtt_client.send_message("leds_green")
        mqtt_client.send_message("right_motor", '600')
        mqtt_client.send_message("stop_motors")
    if b_unscrambled == 'blue':
        mqtt_client.send_message("leds_blue")
        mqtt_client.send_message("left_motor", '600')
        mqtt_client.send_message("stop_motors")
    if p_unscrambled == 'purple':
        mqtt_client.send_message("leds_purple")
        mqtt_client.send_message("right_motor", '600')
        mqtt_client.send_message("stop_motors")



# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
