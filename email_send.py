#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# v0.1 by meigrafd 02.2015
# 
import smtplib

mailServer = 'pop.gmail.com'
mailPort = 587
mailLogin = 'xxx@gmail.com'
mailPass = 'xyz'
mailSendFrom = mailLogin
mailSendTo = 'target@email.com'
mailTLS = True
mailDebug = False

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

if __name__ == '__main__':
	sendemail(mailSendFrom, mailSendTo, 'Bla!', 'Hallo!\nGruesse vom PI')