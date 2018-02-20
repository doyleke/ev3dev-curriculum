import mqtt_remote_method_calls as com
# import robot_controller_mine as robo
import ev3dev.ev3 as ev3
import time
import math

# Old code if feedback from robot was uneeded
# def main():
#     robot = robo.Snatch3r()
#     mqtt_client = com.MqttClient(robot)
#     mqtt_client.connect_to_pc()
#     # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
#     robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


class Ev3Delegate(object):
    """ Delegate that listens for responses from EV3. """
    # initializing the sencsords that were needed for the Deligate class

    def __init__(self):
        self.mqtt_client = None
        self.running = True
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        # self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        # self.pixy = ev3.Sensor(driver_name="pixy-lego")

        # assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.ir_sensor.connected
        # assert self.pixy

        self.led_colors = [ev3.Leds.BLACK, ev3.Leds.GREEN, ev3.Leds.RED]

        self.current_color_index = 0

    # Drives a set distance
    def drive_inches(self, inches_target, speed_deg):

        inches_target = inches_target
        motor_turns = inches_target*90
        speed_deg = speed_deg

        self.right_motor.run_to_rel_pos(position_sp=motor_turns,
                                      speed_sp=speed_deg, stop_action='brake')
        self.left_motor.run_to_rel_pos(position_sp=motor_turns, speed_sp=
        speed_deg, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)


    # Turns a specified amount
    def turn_degrees(self, degrees_to_turn, turn_speed_sp):

            self.left_motor.run_to_rel_pos(speed_sp=(turn_speed_sp),
                                                       position_sp
            =(-degrees_to_turn * 4), stop_action='brake')
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp,
                                            position_sp=degrees_to_turn*4,
                                            stop_action='brake')
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    # Not super needed but used for mobing the arm which is minimal in this
    # code
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

        ev3.Sound.beep().wait()

        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)

        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the
        # motor
        ev3.Sound.beep().wait()

    # Motor Movments

    def stop_motors(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def left_motor(self, left_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        #self.right_motor.stop_action(stop_action='brake')

    def right_motor(self, right_speed):
        self.right_motor.run_forever(speed_sp=right_speed)
        #self.left_motor.stop_action(stop_action='brake')

    def turn_right(self, turn_speed):
        self.right_motor.run_forever(speed_sp=-turn_speed)
        self.left_motor.run_forever(speed_sp=turn_speed)

    def turn_left(self, turn_speed):
        self.right_motor.run_forever(speed_sp=turn_speed)
        self.left_motor.run_forever(speed_sp=-turn_speed)

    def back(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    # Shutting down
    def shutdown(self):

        self.running = False
        self.left_motor.stop_action(stop_action='brake')
        self.right_motor.stop_action(stop_action='brake')
        ev3.Leds.set_color(ev3.Leds.RIGHT, self.led_colors[1])
        ev3.Leds.set_color(ev3.Leds.LEFT, self.led_colors[1])

    def motor_run(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)


    # Not currently in the code.
    def seek_beacon(self):
        beacon_seeker = ev3.BeaconSeeker(channel=1)

        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:

            current_distance = beacon_seeker.distance
            current_heading = beacon_seeker.heading

            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.turn_left(100)

            else:
                if math.fabs(current_heading) <= 2:
                    print("current heading", current_heading)
                    print("On the right heading. Distance: ", current_distance)
                    self.motor_run(forward_speed, forward_speed)
                    while True:
                        current_distance = beacon_seeker.distance
                        if current_distance <=1:
                            self.stop_motors()
                            print('beacon')
                            return True
                        time.sleep(.01)



                elif 2 < math.fabs(current_heading) <= 20:

                    print("current heading: ", current_heading)
                    print("sweet the heading is right. gonna spin now")
                    print("distance: ", current_distance)

                    if current_heading <= 0:
                        self.turn_right(turn_speed)
                    else:
                        self.turn_left(turn_speed)

                elif current_heading > 10:
                    self.turn_left(100)
                    print("Heading too far off")
                    print("current heading:", current_heading)
                elif current_heading < -10:
                    self.turn_right(100)
                    print("Heading too far off")
                    print("current heading:", current_heading)



            time.sleep(0.02)

    # Plays chacha slide audio clip
    def play_song(self):
        ev3.Sound.play("/home/robot/csse120/projects/woodrc"
                       "/ChaCha.wav")

    # Checks for detection of nearby objects with ir camera. Communicates
    # back to PC
    def get_distance(self):
        distance = self.ir_sensor.proximity
        time.sleep(.01)
        self.mqtt_client.send_message("lookaround", [distance])

    def loop_forever(self, mqtt_client):
        self.running = True
        while self.running:
            time.sleep(0.1)


            if self.touch_sensor.is_pressed:
                print("Goodbye!")
                ev3.Sound.speak("Goodbye").wait()
                mqtt_client.close()
                break

    def set_mqtt(self, mqtt_client):
        self.mqtt_client = mqtt_client


def main():
    # Connects the delegates together
    print("Ready")
    robot_delegate = Ev3Delegate()
    mqtt_client = com.MqttClient(robot_delegate)
    robot_delegate.set_mqtt(mqtt_client)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus use EV3 as broker.
    robot_delegate.loop_forever(mqtt_client)


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


main()