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
        Motor.arm(self)
        print(self.motor)
        print('Motor initialized on pin {}'.format(pin))

    def __del__(self):
        Motor.engine_cutoff(self, cutoff=True)
        GPIO.cleanup()
        print('Cleaning up GPIO pins...')

    def arm(self):
        self.motor.start(self.arm_power)
        print('Motor {} ARMED'.format(self.pin))

    def change_power(self, power, runtime=0, auto_cutoff=False):
        if 3 <= power <= self.max_power:
            print('Increasing power to {}'.format(power))
            self.motor.ChangeDutyCycle(power)
            time.sleep(runtime)
            if auto_cutoff:
                Motor.engine_cutoff(self, idle=True)
        else:
            raise ValueError('Max power setting is {}, given power setting was {}'.format(self.max_power, power))

    def engine_cutoff(self, cutoff=False, idle=False):
        if idle:
            print('Back to idle')
            self.motor.start(3)
        elif cutoff:
            print('Turning motor off...')
            self.motor.start(3)
        else:
            print('Action not specifiec, going back to armed position')
            Motor.arm(self)


motor_1 = Motor(12, max_power=12)
value = int(input('Power: '))
motor_1.change_power(value, runtime=2, auto_cutoff=True)
