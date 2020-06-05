import RPi.GPIO as GPIO
import time

p = GPIO.PWM(12, 50)

class Motor:
  def __init__(self, motor):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    self.motor = motor
  def __del__(self):
    GPIO.cleanup()
  def arm(self):
    self.motor.start(3)
  def startup(self):
          for i in range(60, 80, 1):
                  self.motor.ChangeDutyCycle(i/10)
                  time.sleep(0.01)
          time.sleep(0.1)
          self.motor.start(3)
          time.sleep(0.75)
