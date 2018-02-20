import ev3dev.ev3 as ev3
import time
from PIL import Image

import random
from PIL import Image
import mqtt_remote_method_calls as com


class DataContainer(object):
    # Helper class that might be useful to communicate between
    # different callbacks.

    def __init__(self):
        self.running = True

        self.mqtt_client = None
        self.lcd = ev3.Screen()
        self.num_active_dice = 5
        self.max_die_value = 6
        self.consecutive_correct = 0
        self.dice_values = [0, 0, 0, 0, 0]

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

    def randomly_display_new_dice(self):
        self.dice_values = [0, 0, 0, 0, 0]
        for i in range(self.num_active_dice):
            self.dice_values[i] = random.randrange(1, self.max_die_value + 1)
        self.update_lcd()

    def update_lcd(self):
        self.lcd.image.paste(self.dice_images[self.dice_values[0]], (5, 8))
        self.lcd.image.paste(self.dice_images[self.dice_values[1]], (62, 8))
        self.lcd.image.paste(self.dice_images[self.dice_values[2]], (119, 8))
        self.lcd.image.paste(self.dice_images[self.dice_values[3]], (33, 66))
        self.lcd.image.paste(self.dice_images[self.dice_values[4]], (91, 66))
        self.lcd.update()

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

    def guess(self, number_guessed):
        correct_answer = 0
        for value in self.dice_values:
            if value % 2:
                correct_answer += value - 1
                # Even numbers have no stem (dot) in the middle and therefore are not roses.
                # The number 1 has a stem but no "petals" (dots) around it. Value 0
                # The number 3 has a stem and 2 "petals" (dots) around it. Value 2
                # The number 5 has a stem and 4 "petals" (dots) around it. Value 4
                # etc

        if number_guessed == correct_answer:
            print("{} is correct".format(correct_answer))
            if self.num_active_dice == 5:
                self.consecutive_correct += 1
                if self.consecutive_correct >= 3:
                    print("The player has won the game!")
                    self.mqtt_client.send_message("guess_response",
                                                  ["{} is correct! You have won the game!!!!!!!!!!!!!!!!!!".format(
                                                      number_guessed)])
                    ev3.Sound.speak("Correct. You win!").wait()
                    ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()
                    print("Great work! Now let's make the game a bit harder. :)")
                    self.mqtt_client.send_message("guess_response", ["You are done! You can get your checkoff!"])
                    self.mqtt_client.send_message("guess_response", ["Optional: You can now play with more dots. :)"])
                    self.max_die_value = 9  # Make the game a little harder now.
                    self.consecutive_correct = 0
                else:
                    self.mqtt_client.send_message("guess_response",
                                                  ["{} is correct! You have {} correct in a row.".format(
                                                      number_guessed, self.consecutive_correct)])
                    ev3.Sound.speak("correct")
            else:
                self.consecutive_correct = 0
                self.mqtt_client.send_message("guess_response",
                                              ["{} is correct! To win you need 3 wins WITH 5 DICE!".format(
                                                  number_guessed)])
                ev3.Sound.speak("Correct, but only {} dice.".format(self.num_active_dice))
        else:
            too_high_or_too_low = "Too high" if number_guessed > correct_answer else "Too low"
            self.mqtt_client.send_message("guess_response",
                                          ["Your guess of {} was {}. The correct answer for {} is {}".format(
                                              number_guessed, too_high_or_too_low, self.dice_values, correct_answer)])
            self.consecutive_correct = 0
            ev3.Sound.speak(too_high_or_too_low)
            print(too_high_or_too_low)
        self.randomly_display_new_dice()

    def set_number_of_dice(self, number_of_dice):
        if number_of_dice < 1:
            number_of_dice = 1
        elif number_of_dice > 5:
            number_of_dice = 5
        self.num_active_dice = number_of_dice
        self.randomly_display_new_dice()

    def exit(self):
        self.dice_values = [1, 1, 1, 1, 1]
        self.update_lcd()
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


def main():
    print("Ready")
    my_delegate = DataContainer()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus use EV3 as broker.
    my_delegate.loop_forever()
    teary_eyes = Image.open("/home/robot/csse120/assets/images/ev3_lego/eyes_tear.bmp")
    my_delegate.lcd.image.paste(teary_eyes, (0, 0))
    my_delegate.lcd.update()
    print("If you ran via SSH and typed 'sudo chvt 6' earlier, don't forget to type")
    print("'sudo chvt 1' to get Brickman back after you finish this program.")



main()
