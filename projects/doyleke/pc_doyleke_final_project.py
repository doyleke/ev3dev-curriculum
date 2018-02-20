import ev3dev.ev3 as ev3
# import time
from PIL import Image

import robot_controller as robo

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class DataContainer(object):
    # Helper class that might be useful to communicate between
    # different callbacks.

    def __init__(self):
        self.running = True

        # Creates the one and only Screen object and prepares a
        # few Image objects.
        self.lcd_screen = ev3.Screen()

        # All of these images are exactly 178 by 128 pixels,
        # the exact screen resolution
        # They are made by Lego and ship with the Lego Mindstorm
        # EV3 Home Edition software
        # I found the in m3_ir_events_with_the_screen
        self.eyes = Image.open("/home/robot/csse120/assets"
                               "/images/ev3_lego/eyes_neutral.bmp")
        self.angry_eyes = Image.open("/home/robot/csse120/assets"
                                     "/images/ev3_lego/eyes_angry.bmp")
        self.puppy_dog_eyes = Image.open("/home/robot/csse120/assets"
                                         "/images/ev3_lego/"
                                         "eyes_disappointed.bmp")
        self.sad_eyes = Image.open("/home/robot/csse120/assets"
                                   "/images/ev3_lego/eyes_hurt.bmp")
        self.shifty_eyes = Image.open("/home/robot/csse120/assets"
                                      "/images/ev3_lego/eyes_pinch_left.bmp")
        self.progress_0 = Image.open("/home/robot/csse120/assets"
                                     "/images/ev3_lego/progress_bar_0.bmp")
        self.progress_50 = Image.open("/home/robot/csse120/assets"
                                      "/images/ev3_lego/progress_bar_50.bmp")
        self.progress_100 = Image.open("/home/robot/csse120/assets"
                                       "/images/ev3_lego/progress_bar_100.bmp")
        self.teary_eyes = Image.open("/home/robot/csse120/assets"
                                     "/images/ev3_lego/eyes_tear.bmp")
        self.accept = Image.open("/home/robot/csse120/assets"
                                 "/images/ev3_lego/accept.bmp")
        self.bomb = Image.open("/home/robot/csse120/assets"
                               "/images/ev3_lego/Bomb.bmp")
        self.boom = Image.open("/home/robot/csse120/assets"
                               "/images/ev3_lego/Boom.bmp")
        self.decline = Image.open("/home/robot/csse120"
                                  "/assets/images/ev3_lego/Decline.bmp")

        self.dc = DataContainer

    def guess_response(self, string):
        message_from_ev3 = string
        print(message_from_ev3)


def main():
    print("--------------------------------------------")
    print(" Welcome")
    print("--------------------------------------------")

    dc = DataContainer()

    my_delegate = DataContainer()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    display_image(dc.lcd_screen, dc.eyes)
    ev3.Sound.speak("welcome we are happy you joined us today").wait()
    print("Press the touch sensor to exit this program.")

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"

    root = tkinter.Tk()
    root.title("Escape")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame,
                      text='Look at the EV3, then enter a guess for the solution:')
    label.grid(columnspan=2)

    guess_entry = ttk.Entry(main_frame, width=8)
    guess_entry.grid(row=2, column=0)

    guess_button = ttk.Button(main_frame, text="Guess")
    guess_button.grid(row=2, column=1)
    guess_button['command'] = lambda: guess(mqtt_client, guess_entry)
    root.bind('<Return>', lambda event: guess(mqtt_client, guess_entry))

    num_dice_entry = ttk.Entry(main_frame, width=8)
    num_dice_entry.grid(row=3, column=0)

    num_dice_button = ttk.Button(main_frame, text="Set num dice")
    num_dice_button.grid(row=3, column=1)
    num_dice_button['command'] = lambda: game(mqtt_client, num_dice_entry)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=4, column=0)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    e_button = ttk.Button(main_frame, text="Exit on EV3 too")
    e_button.grid(row=4, column=1)
    e_button['command'] = lambda: quit_program(mqtt_client, True)

    root.mainloop()

    if robot.touch_sensor.is_pressed:
        robot_takeover(dc)


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


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        mqtt_client.send_message("exit")
    mqtt_client.close()
    exit()


def game(mqtt, dice):
    print(mqtt)
    print(dice)


main()
