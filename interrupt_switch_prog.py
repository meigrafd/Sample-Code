#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# prog switch v0.2 - by meigrafd
#
# http://www.forum-raspberrypi.de/Thread-prorgammstart-stop-per-taster?pid=149423#pid149423
#
import RPi.GPIO as GPIO
import signal, time, psutil
from subprocess import call

#------------------------------------------------------------------------

shutdownPin = 5 # with GPIO.BOARD pin#5 is gpio3
progswitchPin = 7 # with GPIO.BOARD pin#7 is gpio4

# to use RaspberryPi gpio# (BCM) or pin# (BOARD)
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

#------------------------------------------------------------------------

GPIO.setup(shutdownPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)    #GPIO -> GND
GPIO.setup(progswitchPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  #GPIO -> GND

proz={}
proz['killcount'] = 0

def check_proc_running(procname):
	found = False
	for proc in psutil.process_iter():
		if proc.name() == procname:
			found = True
			break
	return found

def kill_proc(procname):
	done = False
	for proc in psutil.process_iter():
		process = psutil.Process(proc.pid)
		if process.name() == procname:
			try:
				process.terminate()
				process.wait(timeout=3)
				done = True
			except psutil.AccessDenied:
				print "Error: Access Denied to terminate %s" % procname
			except psutil.NoSuchProcess:
				pass
			except psutil.TimeoutExpired:
				if proz['killcount'] == 2:
					print "Error: Terminating of %s failed! (tried 3 times)" % procname
				else:
					print "Error: Terminating of %s took to long.. retrying" % procname
					proz['killcount'] += 1
					kill_proc(procname)
			break
	if done:
		print "%s terminated!" % procname

def start_service(name):
	command = ['/usr/sbin/service', name, 'start'];
	try:
		call(command, shell=False)
		print "%s started!" % name
	except Exception, error:
		print "Error: %s" % error

def shutdown():
	call('poweroff', shell=False)

def interrupt_event(pin):
	zeit = time.strftime("%d.%m.%Y %H:%M:%S")
	if GPIO.input(shutdownPin) == GPIO.HIGH:
		print "[{}]  Shutdown Button {} pressed" . format(zeit, pin)
		shutdown()
	if GPIO.input(progswitchPin) == GPIO.HIGH:
		print "[{}]  Program Switch Button {} pressed" . format(zeit, pin)
		if check_proc_running('mpd'):
			kill_proc('mpd')
			start_service('uv4l')
		elif check_proc_running('uv4l'):
			kill_proc('uv4l')
			start_service('mpd')
		else:
			print "None of the two Programs run!"

try:
	GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=interrupt_event, bouncetime=150)
	GPIO.add_event_detect(progswitchPin, GPIO.BOTH, callback=interrupt_event, bouncetime=150)
	#keep script running
	signal.pause()
except KeyboardInterrupt:
	print "\nQuit\n"
	GPIO.cleanup()
