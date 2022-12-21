"""import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# l298n
in1 = 26
in2 = 16
in3 = 6
in4 = 5
ENA = 25

temps1 = 1

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

GPIO.setup(ENA, GPIO.OUT)
p = GPIO.PWM(ENA, 1000)
p.start(25)


def engine_movement():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    print("dentro")


if __name__ == '__main__':
    engine_movement()
    GPIO.cleanup()"""

# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
import time

from time import sleep

from builtins import input

in1 = 26
in2 = 16
in3 = 6
in4 = 5
ENA = 25
ENB = 24

temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

pa = GPIO.PWM(ENA, 1000)
pb = GPIO.PWM(ENB, 1000)

pa.start(25)
pb.start(25)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")


def get_ldr_sensor(ldr_pin):

    count = 0

    # Output on the pin for
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(ldr_pin, GPIO.IN)

    # Count until the pin goes high
    while GPIO.input(ldr_pin) == GPIO.LOW:
        count += 1

    return count

if __name__ == '__main__':

    while 1:
        print(get_ldr_sensor(4), "LUCES")
        x = input()

        if x == 'r':
            print("run")
            if temp1 == 1:
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
                print("forward")
                x = 'z'
            else:
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
                print("backward")
                x = 'z'

        elif x == 's':
            print("stop")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            x = 'z'

        elif x == 'f':
            print("forward")
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            temp1 = 1
            x = 'z'

        elif x == 'b':
            print("backward")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            temp1 = 0
            x = 'z'

        elif x == 'l':
            print("low")
            pa.ChangeDutyCycle(25)
            pb.ChangeDutyCycle(25)
            x = 'z'

        elif x == 'm':
            print("medium")
            pa.ChangeDutyCycle(50)
            pb.ChangeDutyCycle(50)
            x = 'z'

        elif x == 'h':
            print("high")
            pa.ChangeDutyCycle(75)
            pb.ChangeDutyCycle(75)
            x = 'z'

        elif x == 'e':
            GPIO.cleanup()
            print("GPIO Clean up")
            break

        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")
