"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected

        self.led_colors = [ev3.Leds.BLACK, ev3.Leds.GREEN, ev3.Leds.RED]

        self.current_color_index = 0

    def drive_inches(self, inches_target, speed_deg):

        inches_target = inches_target
        motor_turns = inches_target*90
        speed_deg = speed_deg

        self.right_motor.run_to_rel_pos(position_sp=motor_turns,
                                      speed_sp=speed_deg, stop_action='brake')
        self.left_motor.run_to_rel_pos(position_sp=motor_turns, speed_sp=
        speed_deg, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)


    def turn_degrees(self, degrees_to_turn, turn_speed_sp):

            self.left_motor.run_to_rel_pos(speed_sp=(turn_speed_sp),
                                                       position_sp
            =(-degrees_to_turn * 4), stop_action='brake')
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp,
                                            position_sp=degrees_to_turn*4,
                                            stop_action='brake')
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    # DONE: Implement the Snatch3r class as needed when working the sandox
            # exercises

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)

        while self.touch_sensor.is_pressed == False:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2*360
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        print('made it to arm up')
        self.arm_motor.run_to_rel_pos(position_sp=14.2*360, speed_sp=900)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')

        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)

        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the
        # motor

    def stop_motors(self):
        self.left_motor.stop_action(stop_action='brake')
        self.right_motor.stop_action(stop_action='brake')

    def left_motor(self, left_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.stop_action(stop_action='brake')

    def right_motor(self, right_speed):
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.stop_action(stop_action='brake')

    def back(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)


    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.

        self.running = False
        self.left_motor.stop_action(stop_action = 'brake')
        self.right_motor.stop_action(stop_action = 'brake')
        ev3.Leds.set_color(ev3.Leds.RIGHT, self.led_colors[1])
        ev3.Leds.set_color(ev3.Leds.LEFT, self.led_colors[1])

    def motor_run(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)
