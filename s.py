#!/usr/bin/python
import subprocess
import socket
import sys
from thread import *

HOST = '0.0.0.0'
PORT = 23
PASSWD = 'shutdownPW'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
	sys.exit()
print 'Socket bind complete'

#Start listening on socket
s.listen(1)
print 'Socket now listening'

def _exit():
	close = conn.close()
	close = s.close()
	sys.exit()

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome\r\n') #send only takes string  
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		try:
			#Receiving from client
			data = conn.recv(4096) # Advisable to keep it as an exponent of 2
			line = data.strip() # Remove whitespaces

			if line:
				lenght = len(line)
				print("received: '"+line+"' %s") % lenght
				if line == PASSWD:
					print("Executing shutdown!")
					#subprocess.call(['/sbin/shutdown',"-h","now"])
			else: 
				break
		except (KeyboardInterrupt, SystemExit):
			print "Schliesse Programm.."
			_exit()
	#came out of loop
	conn.close()

#now keep talking with the client
while 1:
	try:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread, (conn,))
	except (KeyboardInterrupt, SystemExit):
		print "Schliesse Programm.."
		_exit()
