import RPi.GPIO as GPIO
import time
import board
from dotenv import load_dotenv
# load_dotenv()
import os
import MySQLdb
from mysql.connector import Error

# scheduler import
from apscheduler.schedulers.background import BlockingScheduler


def upload_stats(connection):
    # UPDATE
    results = connection.promise.query('UPDATE rover SET humidity = 987 WHERE id = 1')

    print(results)


def connect_ddbb():
    # TODO: add the corresponding library
    # load_dotenv()

    connection = MySQLdb.connect(
        host="eu-west.connect.psdb.cloud",
        user="u7tvz6hmep1gpn450v56",
        passwd="pscale_pw_5egEOUrCCRvT0krrKrWMPwSqx6Kc6cGU3fhjxpU39TQ",
        db="liv_stats",
        ssl={
            "ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    )

    try:
        upload_stats(connection)

        """if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select @@version ")
            version = cursor.fetchone()
            if version:
                print('Running version: ', version)
                upload_stats(connection)
        else:
            print('Not connected.')

    except Error as e:
        print("Error while connecting to MySQL", e)"""
    finally:
        connection.close()


if __name__ == '__main__':
    connect_ddbb()
    # sched = BlockingScheduler()
    # sched.add_job(upload_stats(connection), 'interval', seconds=60)  # will do the print_t work for every 60 seconds
    # sched.start()
