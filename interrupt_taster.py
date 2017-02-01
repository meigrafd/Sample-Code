import RPi.GPIO as GPIO
import time
import signal

#------------------------------------------------------------------------
# use the raspi board pin number
#GPIO.setmode(GPIO.BOARD)
# use the gpio number
GPIO.setmode(GPIO.BCM)

# only one of following for GPIO.IN:
PULL = GPIO.PUD_DOWN  #GPIO -> GND
#PULL = GPIO.PUD_UP   #GPIO -> 3V3

Taster = 17
#------------------------------------------------------------------------

GPIO.setup(Taster, GPIO.IN, pull_up_down=PULL)

def cputemp():
	with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
		CPUtemp = int(float(f.readline().split()[0]))
		CPUtemp = round((CPUtemp/1000.0), 2)
	return CPUtemp

def interrupt_event(pin):
	zeit = time.strftime("%d.%m.%Y %H:%M:%S")
	if GPIO.input(Taster) == GPIO.HIGH:
		print "{} Rising edge detected on {}".format(zeit, pin)
		print cputemp()
	else:
		print "{} Falling edge detected on {}".format(zeit, pin)


if __name__ == '__main__':
	try:
		GPIO.add_event_detect(Taster, GPIO.BOTH, callback=interrupt_event, bouncetime=150)
		#keep script running
		signal.pause()
	except (KeyboardInterrupt, SystemExit):
		print "\nQuit\n"
		GPIO.cleanup()