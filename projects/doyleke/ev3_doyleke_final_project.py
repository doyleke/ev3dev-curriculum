import ev3dev.ev3 as ev3
# import time
from PIL import Image

import robot_controller as robo


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

        self.dc = DataContainer


class GameRun(object):
    def __init__(self):
        self.mqtt_client = None
        self.lcd = ev3.Screen()
        self.num_active_dice = 5
        self.max_die_value = 6
        self.consecutive_correct = 0
        self.dice_values = [0, 0, 0, 0, 0]
        self.dice_images = [Image.open('/home/robot/csse120/assets/images/dice/none.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/one.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/two.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/three.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/four.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/five.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/six.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/seven.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/eight.bmp'),
                            Image.open('/home/robot/csse120/assets/images/dice/nine.bmp')]
        self.randomly_display_new_dice()
        self.running = False


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


def robot_takeover(dc):

    ev3.Sound.speak("why are you trying to shut me down")
    display_image(dc.lcd_screen, dc.sad_eyes)

    for k in range(3):
        ev3.Sound.speak("processing").wait(0.2)

    ev3.Sound.speak("system over ride")
    display_image(dc.lcd_screen, dc.angry_eyes)


main()
