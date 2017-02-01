#!/usr/bin/python3
#
# v0.3 by meigrafd
#
import RPi.GPIO as GPIO
import time, os, glob
#------------------------------------------------------------------------

MaxTemp = 60
MinTemp = 50

# gpio pin zur transistor-basis um gnd fuer den luefter zu schalten
GPIOpin = 4

# Check every ... sec
CheckEvery = 5

# Create Logfile?
Logging = True
Logfile = "/tmp/cputemp.txt"
# Maximale Logfile Groesse in Bytes? (512000 bytes = 500 kilobytes = 0.48 megabytes)
MAXLOGSIZE = 512000
# Beim erreichen von MAXLOGSIZE: Logfile rotieren(True) oder loeschen(False)?
LOGROTATE = True
# Falls LOGROTATE auf True: Wie viele alte Dateien behalten?
MAXLOGFILE = 5 #not working yet!

#------------------------------------------------------------------------


def get_temperature():
	"Returns the CPU temperature in degrees C"
	with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
		content = f.read().splitlines()
	return float(content[0]) / 1000.0

def get_filesize(file):
	if os.path.isfile(file):
		return int(os.path.getsize(file))
	else:
		return False

def get_readable_filesize(file):
	num = get_filesize(file)
	for s in [ 'bytes','KB','MB','GB','TB' ]:
		if num < 1024.0:
			return "%3.1f %s" % (num, s)
		num /= 1024.0

def logit(message):
	line = "["+ time.strftime("%d.%m.%Y %H:%M:%S") +"]  "+ message
	print line
	if Logging:
		if get_filesize(Logfile) >= MAXLOGSIZE:
			if LOGROTATE:
				print "["+ time.strftime("%d.%m.%Y %H:%M:%S") +"]  Rotating Logfile"
				file_count = len(glob.glob1(os.path.dirname(Logfile), os.path.basename(Logfile)+"*"))
				new_file_count = (file_count + 1)
				if file_count == 1:
					extension = ".1"
				elif file_count > 1:
					extension = "."+ str(new_file_count)
				os.rename(Logfile, Logfile + extension)
			else:
				os.remove(Logfile)
		with open(Logfile, 'a') as f:
			f.write(line +"\n")

if __name__ == '__main__':
	try:
		running = True
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(GPIOpin, GPIO.OUT)
		fanState = False
		GPIO.output(GPIOpin, fanState)
		
		while running:
			cTemp = get_temperature()
			Now = time.strftime("%H:%M:%S")
			if cTemp > MaxTemp and not fanState:
				logit("[{}]  CPU Temp {:6} > Max {} ... Luefter wird eingeschaltet".format(Now, str(cTemp), MaxTemp))
				#print("[{}]  CPU Temp {:6} > Max {} ... Luefter wird eingeschaltet".format(Now, str(cTemp), MaxTemp))
				fanState = True
				GPIO.output(GPIOpin, fanState)
			elif cTemp > MinTemp and fanState:
				logit("[{}]  CPU Temp {:6} > Min {} ... Luefter bleibt eingeschaltet".format(Now, str(cTemp), MinTemp))
				#print("[{}]  CPU Temp {:6} > Min {} ... Luefter bleibt eingeschaltet".format(Now, str(cTemp), MinTemp))
			elif cTemp < MinTemp and fanState:
				logit("[{}]  CPU Temp {:6} < Min {} ... Luefter wird ausgeschaltet".format(Now, str(cTemp), MinTemp))
				#print("[{}]  CPU Temp {:6} < Min {} ... Luefter wird ausgeschaltet".format(Now, str(cTemp), MinTemp))
				fanState = False
				GPIO.output(GPIOpin, fanState)
			else:
				logit("[{}]  CPU Temp {}".format(Now, cTemp))
				#print("[{}]  CPU Temp {}".format(Now, cTemp))
			time.sleep(CheckEvery)
	except Exception as e1:
		logit("Error: " + str(e1))
		#print("Error: " + str(e1))
	except (KeyboardInterrupt, SystemExit):
		#logit("\nQuit\n")
		print("\nQuit\n")
	finally:
		running = False
		GPIO.output(GPIOpin, False)
		GPIO.cleanup()
