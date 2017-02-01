#!/usr/bin/python
#
# Control Pi over Email - v0.2 - optimized by meigrafd
#
# http://www.forum-raspberrypi.de/Thread-python-scroll-menue?pid=130508#pid130508
#
# first line in email-message must match user defined Password.
# supports multiple commands in each line
#
import picamera, smtplib, sys, time
import email, getpass, imaplib
from time import gmtime, strftime
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#---------------------------------------------------------------------

#check eMails every ... sec
interval = 10
#react only on eMails with exact this subject
subject = 'Pi'
#first line in email-message must match this password to verify authenticity
validpass = 'abc123'

MailReceiveUSER = 'USER'
MailReceivePWD = 'PASSWORD'
MailReceiveSRV = 'imap.gmail.com'

MailSendUSER = MailReceiveUSER
MailSendPWD = MailReceivePWD
MailSendSRV = 'smtp.gmail.com'
MailSendFROM = MailReceiveUSER
MailSendTO = 'xxx'

#---------------------------------------------------------------------

# check Mails
def checkMails():
	try:
		print "Starting checkMails"
		m = imaplib.IMAP4_SSL(MailReceiveSRV)
		m.login(MailReceiveUSER, MailReceivePWD)
		while running:
			m.select("Inbox")
			status, unreadcount = m.status('INBOX', "(UNSEEN)")
			unreadcount = int(unreadcount[0].split()[2].strip(').,]'))
			if unreadcount > 0:
				items = m.search(None, "UNSEEN")
				items = str(items[1]).strip('[\']').split(' ')
				for index, emailid in enumerate(items):
					#print "emailid: " + emailid
					resp, data = m.fetch(emailid, "(RFC822)")
					email_body = data[0][1]
					mail = email.message_from_string(email_body)
					if mail['Subject'] == subject:
						timeNow = strftime("%d.%m.%Y %H:%M:%S", gmtime())
						print "[{}]  New EMail with Subject '{}' received, checking.. ".format(timeNow, mail['Subject']),
						for part in mail.walk():
							if part.get_content_type() == 'text/plain':
								body = part.get_payload()
								#  For each line in message execute instructions
								valid = False
								for line in body.split('\r\n'):
									if line == "":
										#skip empty lines
										continue
									if not valid and line == validpass:
										print "pass is valid!"
										valid = True
									elif not valid and not line == validpass:
										print "\nALERT: first line doesnt match verification password '%s': %s" % (validpass, line)
										break
#---------------------------------------------------------------------
									elif line == "Bild":
										print "Trying to send RaspiCam Pic"
										sendMail( raspicam=True )
									elif line == "Heizung an":
										print line
										#...
#---------------------------------------------------------------------
									else:
										message = "Unknown Command: %s" % line
										print message
										sendMail( msg=message )
			time.sleep(interval)
	except Exception, e1:
		print "Error in checkMails: " + str(e1)
		checkMails()

# Send EMail
def sendMail( subj='Antwort vom Pi', msg='Deine Anfrage', raspicam=False ):
	try:
		if raspicam:
			# Foto erstellen
			fn = 'foto.jpg'
			camera = picamera.PiCamera()
			camera.capture(fn, resize=(640,480))
			camera.close()
		# E-Mail zusammensetzen
		mime = MIMEMultipart()
		mime['From'] = MailSendFROM
		mime['To'] = MailSendTO
		mime['Subject'] = Header(subj, 'utf-8')
		mime.attach(MIMEText(msg, 'plain', 'utf-8'))
		# Bild hinzufuegen
		if raspicam:
			f = open(fn, 'rb')
			img = MIMEImage( f.read() )
			f.close()
			mime.attach(img)
		# Mail versenden
		smtp = smtplib.SMTP(MailSendSRV)
		smtp.starttls()
		smtp.login(MailSendUSER, MailSendPWD)
		smtp.sendmail(MailSendFROM, [MailSendTO], mime.as_string())
		smtp.quit()
	except Exception, e1:
		print "Error in sendMail: " + str(e1)

if __name__ == '__main__':
	try:
		running = True
		checkMails()
	except Exception, e1:
		print "Error...: " + str(e1)
	except (KeyboardInterrupt, SystemExit):
		running = False
		print "Schliesse Programm.."