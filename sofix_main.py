import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import mysql.connector
import threading
from gpiozero import DistanceSensor

GPIO.setmode(GPIO.BCM)

laser = 5
cont = 0
GPIO.setup(laser, GPIO.OUT)

# ldr pin
ldr_pin = 4

# distance sensor
TRIG = 25
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# temp and humidity sensor
dhtPin = 22
dhtDevice = adafruit_dht.DHT11(dhtPin)

# sensors
humidity = 0
temperature_c = 0
light = 0
movement = 0

# ddbb info
ddbb_info = ""


def connect_ddbb():
    # ddbb connection and credentials information
    mydb = mysql.connector.connect(
        host="eu-west.connect.psdb.cloud",
        user="u7tvz6hmep1gpn450v56",
        passwd="pscale_pw_5egEOUrCCRvT0krrKrWMPwSqx6Kc6cGU3fhjxpU39TQ",
        db="liv_stats"
    )

    mycursor = mydb.cursor()

    ddbb_info = [mycursor, mydb]

    return ddbb_info


def get_thread_sensors():
    # The sensors will be continuously working
    while True:
        global light
        global humidity
        global temperature_c

        light = get_ldr_sensor()
        humidity = calc_hum()
        temperature_c = calc_temp()
        print("Temp: {:.1f} C".format(temperature_c))
        print("Humidity: {}%".format(humidity))


def calc_temp():
    return dhtDevice.temperature


def calc_hum():
    return dhtDevice.humidity


def get_ldr_sensor():
    GPIO.setmode(GPIO.BCM)
    count = 0

    # Output on the pin for the ldr
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(ldr_pin, GPIO.IN)

    # Count until the pin goes high to detect luminosity
    while GPIO.input(ldr_pin) == GPIO.LOW:
        count += 1

    return count


def get_thread_bbdd():
    # The database will be updated with the current data every 10 seconds

    global humidity
    global temperature_c
    global light
    global movement

    while True:
        sensors_info = [humidity, temperature_c, light, movement]
        upload_stats(ddbb_info, sensors_info)
        time.sleep(10)


def upload_stats(ddbb_info, sensors_info):
    mycursor = ddbb_info[0]
    mydb = ddbb_info[1]

    humidity_v = str(sensors_info[0])
    temperature_s = str(sensors_info[1])
    light_s = str(sensors_info[2])
    movement_i = str(sensors_info[3])

    sql = "UPDATE rover SET humidity = " + humidity_v + ", light = " + light_s + ", temperature = " + temperature_s + ", movement = " + movement_i + " WHERE id = 1"

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount, "record(s) affected")


def get_thread_dist():
    global movement

    # l298n driver
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

    while True:
        dist = calculate_distance()

        # The distance gathered needs to be multiplied *100 to get it as cm
        dist_ok = dist * 100
        print("dist: ", dist_ok)

        if dist_ok > 25:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            movement = 1
            print("forward")

        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            time.sleep(2)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            time.sleep(2)
            movement = 0
            print("stop!")


def calculate_distance():
    global TRIG
    global ECHO

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    StartTime = time.time()
    StopTime = time.time()

    # The echo detects the triggered signal continuously to calculate the distance

    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StartTime - StopTime

    distance = (TimeElapsed * 34300) / 2

    print("calculate_distance(): ", abs(distance))

    sensor_dist = DistanceSensor(echo=27, trigger=25)

    return sensor_dist.distance


if __name__ == '__main__':
    # Establishment of the connection with the database
    ddbb_info = connect_ddbb()
    GPIO.setmode(GPIO.BCM)

    # Creation of 3 Threads to execute the main functionalities at the same time

    # create a Thread for the sensors (ldr, humidity and temperature)
    thread = threading.Thread(target=get_thread_sensors)
    thread.start()

    # create a Thread fot the bbdd operations
    thread_bbdd = threading.Thread(target=get_thread_bbdd)
    thread_bbdd.start()

    # create a Thread for the distance sensor
    thread_dist = threading.Thread(target=get_thread_dist)
    thread_dist.start()
