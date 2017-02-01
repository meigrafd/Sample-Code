#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Send EMail on GPIO Interrupt
#
# v0.1 (c) by meigrafd
#
# http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email
# http://www.tutorialspoint.com/python/python_sending_email.htm
# http://www.forum-raspberrypi.de/Thread-python-pi2-rpi-gpio-verweigert-gpio4-pin-7-auf-out-und-high
#
import RPi.GPIO as GPIO
import time, signal, smtplib

#---------------------------------------------------------------------
# only one of following:
PULL = GPIO.PUD_DOWN	#GPIO -> GND
#PULL = GPIO.PUD_UP		#GPIO -> 3V3

mailServer = 'pop.gmail.com'
mailPort = 587
mailLogin = 'xxx@gmail.com'
mailPass = 'xyz'
mailSendFrom = mailLogin
mailSendTo = 'target@email.com'
mailTLS = True
mailDebug = True
mailSubject = 'GPIO Aenderung!'
#---------------------------------------------------------------------

RPv = GPIO.RPI_REVISION
if RPv == 1:
	GPIOpins = [0,1,4,17,21,22,10,9,11,14,15,18,23,24,25,8,7]
elif RPv == 2:
	GPIOpins = [2,3,4,17,27,22,10,9,11,14,15,18,23,24,25,8,7]
elif RPv == 3:
	GPIOpins = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for gpin in GPIOpins:
	GPIO.setup(gpin, GPIO.IN, pull_up_down = PULL)


def interrupt_event(pin):
	if GPIO.input(pin):
		msg = "Rising edge detected on GPIO %s" % pin
	else:
		msg = "Falling edge detected on GPIO %s" % pin
	message = time.strftime("%d.%m.%Y %H:%M:%S") + " | " + msg
	print message
	sendemail(mailSendFrom, mailSendTo, mailSubject, message)

def sendemail(from_addr, to_addr, subject, message):
	try:
		header = 'From: %s\n' % from_addr
		header+= 'To: %s\n' % to_addr
		header+= 'Subject: %s\n\n' % subject
		message = header + message
		conn = smtplib.SMTP(mailServer, mailPort)
		if mailDebug:
			conn.set_debuglevel(True) #show communication with the server
		if mailTLS:
			conn.starttls()
		conn.login(mailLogin, mailPass)
		error = conn.sendmail(from_addr, to_addr, message)
		if not error:
			print "Successfully sent email"
	except Exception, e:
		print "\nSMTP Error: " + str(e)
	finally:
		if conn:
			conn.quit()


try:
	for gpin in GPIOpins:
		GPIO.add_event_detect(gpin, GPIO.BOTH, callback=interrupt_event, bouncetime=150)
	
	#keep script running
	signal.pause()

except (KeyboardInterrupt, SystemExit):
	print "\n..Quitting..\n"
except Exception, e:
	print "\nError: " + str(e)
finally:
	GPIO.cleanup()

