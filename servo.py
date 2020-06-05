import RPi.GPIO as GPIO
import time


class Servo:
    def __init__(self, pin=12, max_low=11, max_high=4, center=6.6):
        self.pin = pin
        self.max_low = max_low
        self.max_high = max_high
        self.center = center
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)  # creating servo object at designated pin

    def __del__(self):
        self.servo.start(self.center)
        GPIO.cleanup()
        print('Cleaning up GPIO pins...')

    def arm(self, level=False):
        if level:
            self.servo.ChangeDutyCycle(self.center)
            time.sleep(0.5)
        elif not level:
            print('ARMING servo at pin {}, going to center position'.format(self.pin))
            self.servo.ChangeDutyCycle(self.center)
            time.sleep(0.5)

    def pre_flight_check(self, order=0):
        if order == 0:
            time.sleep(0.5)
            print('LOW')
            self.servo.ChangeDutyCycle(self.max_low)
            time.sleep(0.5)
            print('UP')
            self.servo.ChangeDutyCycle(self.max_high)
        elif order == 1:
            time.sleep(0.5)
            print('LOW')
            self.servo.ChangeDutyCycle(self.max_high)
            time.sleep(0.5)
            print('UP')
            self.servo.ChangeDutyCycle(self.max_low)
        time.sleep(0.5)
        print('CENTER')
        self.servo.ChangeDutyCycle(self.center)
        time.sleep(0.5)

    def change_pos(self, pos):
        mp = [self.max_low, self.max_high]
        print('Max up: {}\nMax down: {}'.format(mp[0], mp[1]))
        if mp[1] <= pos <= mp[0]:
            self.servo.ChangeDutyCycle(pos)
            print("Pos changed to {}".format(pos))
        else:
            raise ValueError("Position Unreachable! max low and high are {}, given position was {}".format(mp, pos))


right_servo = Servo(12)
right_servo.arm()
right_servo.pre_flight_check(order=0)
