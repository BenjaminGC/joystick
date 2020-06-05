import RPi.GPIO as GPIO
import time


class Motor:
  def __init__(self, pin=12):
    self.pin = pin
    self.max_power = 8                                # Truelly 8?
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.pin, GPIO.OUT)
    self.motor = GPIO.PWM(self.pin, 50)
    print('Motor initialized on pin {}'.format(pin))
    
  def __del__(self):
    GPIO.cleanup()
    print('Cleaning up GPIO pins...')
    
  def arm(self):
    self.motor.start(3)
    print('Motor {} ARMED'.format(self.pin))
    
  def change_power(self, power):
    print('Increasing power to {}'.format(power))
    self.motor.ChangeDutyCycle(power)
  
  def engine_cutoff(self):
    print('Turning motor off...')
    self.motor.start(3)
    

