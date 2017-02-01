#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# v0.2 by meigrafd
#
# http://www.forum-raspberrypi.de/Thread-python-python-script-funktioniert-nach-dem-start-nach-einiger-zeit-nicht-mehr?pid=134304#pid134304 
#
# http://jigfoot.com/hatworshipblog/?p=60
#
import sys
from time import *
import mpd
import RPi.GPIO as GPIO
import signal
#------------------------------------------------------------------------

MPD_HOST     = "localhost"
MPD_PORT     = "6600"
MPD_PASSWORD = "volumio"   # password for Volumio / MPD

#------------------------------------------------------------------------

# to use RaspberryPi gpio# (BCM) or pin# (BOARD)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

#GPIO pins
GPIO_PlayStop    = 17
GPIO_VolumePlus  = 27
GPIO_VolumeMinus = 22
GPIO_PlayNext    = 23
GPIO_PlayPrev    = 24

# only one of following:
PULL = GPIO.PUD_DOWN	#GPIO -> GND
#PULL = GPIO.PUD_UP		#GPIO -> 3V3

# set up GPIO input channels
GPIO.setup(GPIO_PlayStop,    GPIO.IN, pull_up_down=PULL)
GPIO.setup(GPIO_VolumePlus,  GPIO.IN, pull_up_down=PULL)
GPIO.setup(GPIO_VolumeMinus, GPIO.IN, pull_up_down=PULL)
GPIO.setup(GPIO_PlayNext,    GPIO.IN, pull_up_down=PULL)
GPIO.setup(GPIO_PlayPrev,    GPIO.IN, pull_up_down=PULL)

#------------------------------------------------------------------------

def connectMPD(client):
	try:
		client.timeout = 10
		client.connect(MPD_HOST, MPD_PORT)
	except mpd.ConnectionError, err:
		if "Already connected" in err:
			print err
			return True, None
		else:
			return False, err
	if MPD_PASSWORD:
		try:
			client.password = MPD_PASSWORD
		except mpd.CommandError, err:
			disconnectMPD(client)
			return False, err
	return True, None

def disconnectMPD(client):
	try:
		client.disconnect()
	except mpd.ConnectionError:
		pass

def reconnectMPD(client):
	connected = False
	while not connected:
		connected, error = connectMPD(client)
		if not connected:
			print "Error: %s" % error
			print "Couldn't connect. Retrying"
			sleep(5)
	return connected

def _ping(client):
	try:
		client.ping()
	except mpd.ConnectionError, e:
		con = reconnectMPD(client)

def Interrupt_event(pin):
	_ping(client)
	PlayStat = client.status()
	if GPIO.input(Play) == GPIO.HIGH:
		if PlayStat['state'] == "stop" or PlayStat['state'] == "pause":
			client.load("MyRadio")
			client.play()
		elif PlayStat['state'] == "play":
			client.stop()
			client.clear()
	elif GPIO.input(Lauter) == GPIO.HIGH:
		vol = int(PlayStat['volume'])
		if vol >= 95:
			client.setvol(100)
		else:
			SetVol = vol + 5
			client.setvol(SetVol) 
	elif GPIO.input(Leiser) == GPIO.HIGH:
		vol = int(PlayStat['volume'])
		if vol <= 5:
			client.setvol(0)
		else:
			SetVol = vol - 5
			client.setvol(SetVol) 
	elif GPIO.input(Next) == GPIO.HIGH:
		client.next()
		client.play()
	elif GPIO.input(Prev) == GPIO.HIGH:
		client.previous()
		client.play()
	else:
		print "ERROR! Unknown GPIO pin triggered: %s" % pin

#------------------------------------------------------------------------


try:
	GPIO.add_event_detect(Play, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(Lauter, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(Leiser, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(Next, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
	GPIO.add_event_detect(Prev, GPIO.RISING, callback=Interrupt_event, bouncetime=150)
	client = mpd.MPDClient()
	connected, error = connectMPD(client)
	if error:
		print error
		raise SystemExit

	#keep script running
	signal.pause()
except (KeyboardInterrupt, SystemExit):
	disconnectMPD(client)
	GPIO.cleanup()
	print "\nQuit\n"
