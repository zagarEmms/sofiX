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

# distance sensor
TRIG = 17
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# temp and humidity sensor
dhtDevice = adafruit_dht.DHT11(board.D22)

#l298n
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

def calculate_distance():
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


def calc_temp():
    return dhtDevice.temperature


def calc_hum():
    return dhtDevice.humidity


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


def turn(turnb):
    if turnb:
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        time.sleep(2)

    else:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        time.sleep(2)

    return not turnb


if __name__ == '__main__':
    # servo_laser_work()
    turnb = False

    while True:
        try:
            """humidity = calc_hum()
            temperature_c = calc_temp()
            print("Temp: {:.1f} C".format(temperature_c))
            print("Humidity: {}%".format(humidity))

            dist = calculate_distance()

            if humidity > 45:
                GPIO.output(led, True)
            else:
                GPIO.output(led, False)

            if dist < 20:
                GPIO.output(laser, True)
            else:
                GPIO.output(laser, False)

            time.sleep(2)
        """
            dist = calculate_distance()
            if dist < 10:
                turn(turnb)

            GPIO.cleanup()
        except RuntimeError as error:
            print(error.args[0])
