import RPi.GPIO as GPIO
import time
import board
import time

GPIO.setmode(GPIO.BCM)

ldr_pin = 4


def get_ldr_sensor():
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
        print(count)

    return count


if __name__ == '__main__':
    while True:
        get_ldr_sensor()
