#
# http://www.forum-raspberrypi.de/Thread-php-interrupt-ueber-apache-an-python-script-senden?pid=122550#pid122550
#
import signal
import sys

def signal_handler(signal, frame):
    print('Script Interrupted! (Control-C)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()