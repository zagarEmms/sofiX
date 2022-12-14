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

# servo
servoPin = 22
GPIO.setup(servoPin, GPIO.OUT)
GPIO.output(servoPin, GPIO.LOW)
p = GPIO.PWM(servoPin, 50)
p.start(0)

# temp and humidity sensor
dhtDevice = adafruit_dht.DHT11(board.D22)

# l298n
in1 = 26
in2 = 16
in3 = 6
in4 = 5
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)


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


def servo_laser_work():
    p.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    print("1")
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    print("2")
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    print("3")
    p.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    print("4")
    p.ChangeDutyCycle(10)
    time.sleep(0.5)
    print("5")
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    print("6")
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    print("7")
    p.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    print("8")


def motor_movement():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)


if __name__ == '__main__':
    # servo_laser_work()
    motor_movement()

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
            GPIO.cleanup()
        except RuntimeError as error:
            print(error.args[0])
