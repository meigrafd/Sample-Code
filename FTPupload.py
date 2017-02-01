#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# v0.21 by meigrafd
#
# requires ftputil >= v3.2
#
# apt-get install python-pip && pip install ftputil
#
#ftputil docu: http://ftputil.sschwarzer.net/trac/wiki/Documentation

import time
import sys
import os
import ftputil

##----- CONFIG - START ----------------------------------------

ftpHost = "192.168.0.11"
ftpPort = 21
ftpUser = 'pi'
ftpPass = 'raspberry'
ftpRemoteDir = '/'

##----- CONFIG - END ------------------------------------------


def logError(message):
	try:
		sys.stderr.write(message + "\n")
	except UnicodeEncodeError:
		sys.stderr.write(message.encode("utf8") + "\n")

def connectFtp():
	connected = True
	ftp = None
	try:
		ftp = ftputil.FTPHost(ftpHost, ftpUser, ftpPass, port=ftpPort)
	except OSError, e:
		print >> sys.stderr, 'Got error: "%s"' % e
		connected = False
	return ftp, connected

def progress(chunk):
	global received_size
	received_size += len(chunk)
	print("Uploading Progress: {} kB / {} kB".format(float(received_size)/1024, total_size))

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: %s <file>" % sys.argv[0])
		sys.exit(1)
	localFile = sys.argv[1]
	ftp = None
	received_size = 0
	try:
		total_size = float(os.path.getsize(localFile))/1024 #kB
		ftp, connected = connectFtp()
		if not connected:
			print >> sys.stderr, 'Cant connect to remote! Exiting Script'
			sys.exit(1)
		#remove all whitespace characters (space, tab, newline, and so on)
		remotePath = ftpRemoteDir.rstrip('/')
		remoteFile = remotePath+"/"+localFile
		#change to remote dir
		try:
			ftp.chdir(remotePath)
		except OSError, e:
			logError("Remote Directory {} doesnt Exists!".format(remotePath))
			raise
		#upload file
		try:
			ftp.upload(localFile, remoteFile, callback=progress)
		except Exception:
			logError("Upload failed!")
			raise
	except Exception, e:
		logError("Error: %s" % (e))
	except ftputil.error.PermanentError, e:
		logError("Permanent Error occurred: %s") % (e)
	except (KeyboardInterrupt, SystemExit):
		print("\nSchliesse Programm..\n")
	finally:
		if ftp:
			ftp.close()