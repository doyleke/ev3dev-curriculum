import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
from PIL import Image
import time


class Game(object):
    # Class to communicate between different callbacks.

    def __init__(self):
        self.running = True

        # Creates the Screen object and prepares Image objects.
        self.lcd_screen = ev3.Screen()

        # All of these images are exactly 178 by 128 pixels,
        # the exact screen resolution
        # They are made by Lego and ship with the Lego Mindstorm
        # EV3 Home Edition software
        # I found the in m3_ir_events_with_the_screen and the assets

        self.eyes = Image.open("/home/robot/csse120/assets"
                               "/images/ev3_lego/eyes_neutral.bmp")
        self.accept = Image.open("/home/robot/csse120/assets"
                                 "/images/ev3_lego/accept.bmp")
        self.decline = Image.open("/home/robot/csse120"
                                  "/assets/images/ev3_lego/Decline.bmp")

# ----------------------------------------------------------------------
# Helper Screen function for putting an image on the screen.
# ----------------------------------------------------------------------


def display_image(lcd_screen, image):
    # Function to put an image on the screen.  All images used with this
    # function should be full screen images.
    # The screen is 178 by 128 pixels.

    lcd_screen.image.paste(image, (0, 0))
    lcd_screen.update()


def main():

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    game = Game()

    game.eyes()

    rc1 = ev3.RemoteControl(channel=1)
    rc2 = ev3.RemoteControl(channel=2)

    finish_line(ev3.ColorSensor.COLOR_BLACK)
    water_bottle()

    game.accept()

    # This sets up our buttons for the IR remote

    btn = ev3.Button()
    rc1.on_red_up = lambda state: forward_left_motor(state, robot)
    rc1.on_red_down = lambda state: back_left_motor(state, robot)
    rc1.on_blue_up = lambda state: forward_right_motor(state, robot)
    rc1.on_blue_down = lambda state: back_right_motor(state, robot)
    ev3.on_backspace = lambda state: handle_shutdown(state, game)

    rc2.on_red_up = lambda state: handle_arm_up_button(state, robot)
    rc2.on_red_down = lambda state: handle_arm_down_button(state, robot)
    rc2.on_blue_up = lambda state: handle_calibrate_button(state, robot)
    rc2.on_blue_down = lambda state: handle_shutdown(state, game)

    ev3.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    ev3.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    while game.running:
        btn.process()
        rc1.process()
        rc2.process()
        time.sleep(0.01)


def finish_line(color_to_seek):

    # This function tells the motor when it reaches the finish line
    # by using the color sensor reading the black squares.
    # It then tells the motors to slow down and the
    robot = robo.Snatch3r()

    robot.motor_run(500, 500)
    while True:
        current_color = robot.color_sensor.color
        print(current_color)
        if current_color == color_to_seek:
            robot.motor_run(100, 100)
            ev3.Sound.speak("Finish line")
            time.sleep(1.0)
            # This sleep allows it to get past the finish line
            # because it is checkered and the second row of black
            # squares will set it off again

        break


def water_bottle():

    # This function uses the IR sensor to find the water bottle.
    # It stops motors, raises the arm up, and speaks.

    robot = robo.Snatch3r

    while not robot.touch_sensor.is_pressed:
        if robot.ir_sensor.proximity < 10:
            ev3.Sound.beep().wait()
            print(robot.ir_sensor.proximity)
            time.sleep(1.5)
            robot.stop_motors()
            ev3.Sound.beep()
            robot.arm_up()
            ev3.Sound.speak("we did it")

        time.sleep(0.1)

    robot.loop_forever()


# all of these are for driving with the IR remote


def forward_left_motor(button_state, robot):

    if button_state:
        ev3.Leds.set_color(ev3.Leds.LEFT, robot.led_colors[1])
        robot.left_motor.run_forever(speed_sp=600)
        print("up red button pressed")

    else:
        ev3.Leds.set_color(ev3.Leds.LEFT, robot.led_colors[0])
        robot.left_motor.run_forever(speed_sp=0)
        print("up red button was released")


def back_left_motor(button_state, robot):

    if button_state:
        ev3.Leds.set_color(ev3.Leds.LEFT, robot.led_colors[2])
        robot.left_motor.run_forever(speed_sp=-600)
        print("down red button pressed")

    else:
        ev3.Leds.set_color(ev3.Leds.LEFT, robot.led_colors[0])
        robot.left_motor.run_forever(speed_sp=0)
        print("down red button was released")


def forward_right_motor(button_state, robot):

    if button_state:
        ev3.Leds.set_color(ev3.Leds.RIGHT, robot.led_colors[1])
        robot.right_motor.run_forever(speed_sp=600)
        print("up blue button pressed")

    else:
        ev3.Leds.set_color(ev3.Leds.RIGHT, robot.led_colors[0])
        robot.right_motor.run_forever(speed_sp=0)
        print("up blue button was released")


def back_right_motor(button_state, robot):

    if button_state:
        ev3.Leds.set_color(ev3.Leds.RIGHT, robot.led_colors[2])
        robot.right_motor.run_forever(speed_sp=-600)
        print("down blue button pressed")

    else:
        ev3.Leds.set_color(ev3.Leds.RIGHT, robot.led_colors[0])
        robot.right_motor.run_forever(speed_sp=0)
        print("down blue button was released")


def handle_arm_up_button(button_state, robot):
    """
    Moves the arm up when the button is pressed.
    """
    if button_state:
        robot.arm_up()


def handle_arm_down_button(button_state, robot):
    """
    Moves the arm down when the button is pressed.
    """
    if button_state:
        robot.arm_down()


def handle_calibrate_button(button_state, robot):
    """
    Has the arm go up then down to fix the starting position.
    """
    if button_state:
        robot.arm_calibration()


def handle_shutdown(button_state, dc):
    """
    Exits the program.
    """
    if button_state:
        dc.running = False



main()
