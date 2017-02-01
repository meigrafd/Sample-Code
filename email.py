#!/usr/bin/python
# -*- coding: utf-8 -*-
import poplib
from email import parser
import subprocess
import time

### CONFIG - START
mailServer = 'pop.gmail.com'
mailPort = 995
mailLogin = 'xxx@gmail.com'
mailPass = 'xyz'
mailDebug = 2   #0 , 1 , >=2
ReactOnSubject = 'Bild'
RunCommand = './mailcam.py'
### CONFIG - END

def connectMail():
	global pop_conn
	pop_conn = poplib.POP3_SSL(mailServer, mailPort)
	pop_conn.set_debuglevel(mailDebug)
	try:
		pop_conn.user(mailLogin)
		pop_conn.pass_(mailPass)
		print("Logged in %s as %s" % (mailServer, mailLogin))
		return True
	except:
		print("Error connecting "+ mailServer)
		return False

def getMails():
	# get general information (msg_count, box_size)
	stat = pop_conn.stat()
	print("Status: %d message(s), %d bytes" % stat)
	maillist = pop_conn.list()[1]
	#Get messages from server:
	messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
	#Concat message pieces:
	messages = ["\n".join(msg[1]) for msg in messages]
	#Parse message into an email object:
	messages = [parser.Parser().parsestr(msg) for msg in messages]
	return messages

if connectMail():
	try:
		while True:
			msgs = getMails()
			for message in msgs:
				if ReactOnSubject in message['subject']:
					print(message['subject'])
					subprocess.call(RunCommand, shell=True)
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nQuit\n")
	except:
		print("Error!")

pop_conn.quit()
