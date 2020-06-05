import RPi.GPIO as GPIO
import time


class Motor:
    def __init__(self, pin=12, max_power=8, arm_power=3):
        self.pin = pin
        self.max_power = max_power  # Truelly 8?
        self.arm_power = arm_power
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.motor = GPIO.PWM(self.pin, 50)
        print('Motor initialized on pin {}'.format(pin))

    def __del__(self):
        Motor.engine_cutoff(self)
        GPIO.cleanup()
        print('Cleaning up GPIO pins...')

    def arm(self):
        self.motor.start(self.arm_power)
        print('Motor {} ARMED'.format(self.pin))

    def change_power(self, power, runtime=0):
        if 3 <= power <= self.max_power:
            print('Increasing power to {}'.format(power))
            self.motor.ChangeDutyCycle(power)
            time.sleep(runtime)
        else:
            raise ValueError('Max power setting is {}, given power setting was {}'.format(self.max_power, power))

    def engine_cutoff(self):
        print('Turning motor off...')
        self.motor.start(3)


motor_1 = Motor(12, max_power=10)
value = int(input('Power: '))
motor_1.change_power(value, runtime=2)
