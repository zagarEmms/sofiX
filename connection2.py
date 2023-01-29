import mysql.connector
from apscheduler.schedulers.background import BlockingScheduler


def connect_ddbb():
    mydb = mysql.connector.connect(
        host="eu-west.connect.psdb.cloud",
        user="u7tvz6hmep1gpn450v56",
        passwd="pscale_pw_5egEOUrCCRvT0krrKrWMPwSqx6Kc6cGU3fhjxpU39TQ",
        db="liv_stats"
    )

    mycursor = mydb.cursor()

    ddbb_info = [mycursor, mydb]

    return ddbb_info


def upload_stats(ddbb_info):
    mycursor = ddbb_info[0]
    mydb = ddbb_info[1]

    sql = "UPDATE rover SET humidity = '1' WHERE id = 1"

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount, "record(s) affected")


if __name__ == '__main__':
    ddbb_info = connect_ddbb()
    #upload_stats(ddbb_info)

    sched = BlockingScheduler()
    sched.add_job(upload_stats, 'interval', args=[ddbb_info], seconds=10)
    sched.start()
