import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)
down=11
center=6.6
up=4
p.start(center)

def test_max(pin):
        time.sleep(0.5)
        pin.ChangeDutyCycle(down)
        time.sleep(0.5)
        pin.ChangeDutyCycle(up)
        time.sleep(0.5)
        pin.ChangeDutyCycle(center)
        time.sleep(0.5)
        GPIO.cleanup()
        print("Done")


def change_pos(pin):
        pos=float(input('change pos to: '))
        if up<=pos<=down:
                pin.ChangeDutyCycle(pos)
                print("Pos changed to {}".format(pos))
        else:
                print("Position unreachable")

def change_pos_test(pin):
        x=4
        while x<=10:
                pin.ChangeDutyCycle(x)
                print("Servo pos: {}".format(x))
                x+=0.1
                time.sleep(0.1)

        while x>=4:
                pin.ChangeDutyCycle(x)
                print("Servo pos: {}".format(x))
                x-=0.1
                time.sleep(0.1)

while True:
        try:
                test_max(p)
        except KeyboardInterrupt:
                p.ChangeDutyCycle(center)
                time.sleep(0.5)
                print("exit")
                GPIO.cleanup()
                break

