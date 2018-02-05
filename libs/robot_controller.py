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

        self.arm_motor.position = 0  # Calibrate the down position as 0 (
        # this line is
        # correct as is).

    def arm_up(self):
        """
    Moves the Snatch3r arm to the up position.

    Type hints:
      :type arm_motor: ev3.MediumMotor
      :type touch_sensor: ev3.TouchSensor
    """
    # DONE: 4. Implement the arm up movement by fixing the code below
    # Command the arm_motor to run forever in the positive direction at max speed.
    # Create a while loop that will block code execution until the touch sensor is pressed.
    #   Within the loop sleep for 0.01 to avoid running code too fast.
    # Once past the loop the touch sensor must be pressed. Stop the arm motor using the brake stop action.
    # Make a beep sound

    # Code that attempts to do this task but has many bugs.  Fix them!

        self.arm_motor.run_to_rel_pos(position_sp=14.2*360, speed_sp=900)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')

        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_down(self):
        """
    Moves the Snatch3r arm to the down position.

    Type hints:
      :type arm_motor: ev3.MediumMotor
    """
    # DONE: 5. Implement the arm up movement by fixing the code below
    # Move the arm to the absolute position_sp of 0 at max speed.
    # Wait until the move completes
    # Make a beep sound

    # Code that attempts to do this task but has bugs.  Fix them.
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)

        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the
        # motor

