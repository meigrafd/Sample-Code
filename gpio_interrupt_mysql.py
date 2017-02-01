#!/usr/bin/python
#
# http://www.forum-raspberrypi.de/Thread-gpio-status-in-mysql-datenbank-schreiben?pid=244059#pid244059
#

from __future__ import print_function
from RPi import GPIO
import Queue # https://pymotw.com/2/Queue/
import MySQLdb
import time
import sys

mysqlHost = '127.0.0.1'
mysqlPort = 3306
mysqlLogin = 'root'
mysqlPass = 'raspberry'
mysqlDatabase = 'volkszaehler'

gpio_list = [2, 3, 4, 17, 27, 22, 10, 9, 11, 18, 23, 24, 25, 8, 7]

GPIO.setmode(GPIO.BCM)


# Pro Status (GPIO HIGH oder GPIO LOW) ein Queue erstellen
queue_high = Queue.Queue()
queue_low = Queue.Queue()


class DB(object):
    def __init__(self, host, port, user, passwd, db):
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
    
    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor


# ISR
def interrupt_Event(channel):
    if GPIO.input(channel) == GPIO.HIGH:
        queue_high.put(channel)
    else:
        queue_low.put(channel)


try:
    db = DB(host=mysqlHost, port=mysqlPort, user=mysqlLogin, passwd=mysqlPass, db=mysqlDatabase)
    # Interrupt Event fuer jeden gpio hinzufuegen. Auf steigende und fallende Flanke reagieren und ISR deklarieren sowie Pin entprellen
    for gpio in gpio_list:
        GPIO.setup(gpio, GPIO.IN)
        GPIO.add_event_detect(gpio, GPIO.BOTH, callback=interrupt_Event, bouncetime=200)
    
    # Queues abarbeiten
    while True:
        time.sleep(0.1)
        if not queue_high.empty():
            pin = queue_high.get()
            print("GPIO HIGH: %s" % pin)
            cur = db.query("INSERT INTO data (channel_id(%s)) (timestamp, value) VALUES (%s, %s);" % (pin, time.time(), '1'))
        if not queue_low.empty():
            pin = queue_low.get()
            print("GPIO LOW: %s" % pin)
            cur = db.query("INSERT INTO data (channel_id(%s)) (timestamp, value) VALUES (%s, %s);" % (pin, time.time(), '0'))
    
except (KeyboardInterrupt, SystemExit):
    GPIO.cleanup()
    print("\nQuit\n")
