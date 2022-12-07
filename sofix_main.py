import RPi.GPIO as GPIO
import time
import board
import adafruit_dht

GPIO.setmode(GPIO.BCM)
led = 4
laser = 5
cont = 0
GPIO.setup(led, GPIO.OUT)
GPIO.setup(laser, GPIO.OUT)

TRIG = 17
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

dhtDevice = adafruit_dht.DHT11(board.D22)


def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StartTime - StopTime

    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':

    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print("Temp: {:.1f} C".format(temperature_c))
            print("Humidity: {}%".format(humidity))

            dist = distance()

            if humidity > 45:
                GPIO.output(led, True)
            else:
                GPIO.output(led, False)

            if dist < 20:
                GPIO.output(laser, True)
            else:
                GPIO.output(laser, False)


        except RuntimeError as error:
            print(error.args[0])
        time.sleep(2)
