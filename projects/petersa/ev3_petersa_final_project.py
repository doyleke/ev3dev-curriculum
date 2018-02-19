
import time
import ev3dev.ev3 as ev3

import mqtt_remote_method_calls as com


class Ev3delegate(object):
    """ This class is the same as robot_controller but is modified so that
    it does not interfere with other team member projects. This class is
    specifically for the robot, and therefore defines functions that
    control the robots actions. """

    def __init__(self):

        # The code below connects all of the robots sensors and motors to
        # specific variables
        self.mqtt_client = None
        self.running = True
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        # Then is assures that all sensors and motors are connected properly
        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.ir_sensor.connected
        assert self.pixy

    def set_mqtt(self, mqtt_client):

        # This code establishes a single mqtt_client that can be called in
        # different function/ parts of code.
        self.mqtt_client = mqtt_client

    def stop_motors(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def drive_inches(self, inches_target, speed_deg):

        # The following code was copied from the robot_controller
        inches_target = inches_target
        motor_turns = inches_target*90
        speed_deg = speed_deg

        self.right_motor.run_to_rel_pos(position_sp=motor_turns,
                                        speed_sp=speed_deg,
                                        stop_action='brake')
        self.left_motor.run_to_rel_pos(position_sp=motor_turns,
                                       speed_sp=speed_deg, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):

            # The following code was copied from the robot_controller
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp,
                                           position_sp=(-degrees_to_turn * 4),
                                           stop_action='brake')
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp,
                                            position_sp=degrees_to_turn*4,
                                            stop_action='brake')
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def drive_shapes(self, sides, fill_color, outline_color):
        # The code below was modified in order for the robot to drive the
        # number of sides that was passed in.

        print('made it to drive_shapes')
        # The following code makes the robot drive in a circle if the number
        #  of sides is zero
        if sides == 0:
            self.left_motor.run_to_rel_pos(speed_sp=400, position_sp=(-360 *
                                                                      4),
                                           stop_action='brake')
            self.right_motor.run_to_rel_pos(speed_sp=400,
                                            position_sp=360*4,
                                            stop_action='brake')
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        else:
            turn_amount = 360/sides
            for k in range(sides):
                self.drive_inches(5, 500)
                self.turn_degrees(turn_amount, 500)

        # The code below assures that the robot has made it to the code and
        # sends a message back to the pc calling the things_to_draw function
        print('connecting to pc')
        self.mqtt_client.send_message('things_to_draw', [sides, fill_color,
                                                         outline_color])

    def loop_forever(self, mqtt_client):
        self.running = True
        while self.running:
            time.sleep(0.1)

            # The following code exits the program on the ev3 side when the
            # touch sensor is pressed
            if self.touch_sensor.is_pressed:
                print("Goodbye!")
                ev3.Sound.speak("Goodbye").wait()
                mqtt_client.close()
                break

            # The following code stops the motors, beeps, and prints a message
            # when an object is detected within a certain range
            if self.ir_sensor.proximity < 10:
                self.stop_motors()
                ev3.Sound.beep().wait()
                print('Cannot complete drawing')
                time.sleep(1.5)
            time.sleep(0.1)


def main():
    robot = Ev3delegate()   # This code establishes the robot as an Ev3delegate
    mqtt_client = com.MqttClient(robot)  # This code constructs a mqtt client
    robot.set_mqtt(mqtt_client)
    mqtt_client.connect_to_pc()  # This code connects the robot to the pc
    robot.loop_forever(mqtt_client)


main()
