import RPi.GPIO as GPIO
import time

class Servo:
        def __init__(self, pin=12, max_low=11, max_high=4, center=4):
                self.pin = pin
                self.max_low = max_low
                self.max_high = max_high
                self.center = center
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.pin, GPIO.OUT)
                self.servo = GPIO.PWM(self.pin, 50)     # creating servo object at designated pin
        
        def __del__(self):
                Servo.change_pos(self, level=True)
                GPIO.cleanup()
                print('Cleaning up GPIO pins...')
                
        def arm(self):
                print('ARMING servo at pin {}, going to center position'.format(self.pin))
                self.servo.start(self.center)
        
        def pre_flight_check(self, order=0):
                if order == 0:
                        self.servo.ChangeDutyCycle(self.max_low)
                        time.sleep(0.5)
                        self.servo.ChangeDutyCycle(self.max_high)
                if order == 1:
                        self.servo.ChangeDutyCycle(self.max_high)
                        time.sleep(0.5)
                        self.servo.ChangeDutyCycle(self.max_low)
                time.sleep(0.5)
                self.servo.ChangeDutyCycle(self.center)

        def change_pos(self, pos, level=False):
                if not level:
                        mp = [self.max_low, self.max_high]
                        print('Max up: {}\nMax down: {}'.format(mp[0], mp[1]))
                        pos=float(input('change pos to: '))
                        if mp[0] <= pos <= mp[1]:
                                self.servo.ChangeDutyCycle(pos)
                                print("Pos changed to {}".format(pos))
                        else:
                                raise ValueError("Position Unreachable! max low and high are {}, given position was {}".format(mp, pos))
                elif level:
                        print('servo at pin {} going to center position'.format(self.pin))
                        self.servo.start(self.center)


right_servo = Servo(12)
right_servo.arm()
right_servo.pre_flight_check(order=0)
right_servo.pre_flight_check(order=1)
