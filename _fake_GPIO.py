from __future__ import print_function

print('nix_GPIO loaded - testing without hardware')

RPI_REVISION = 1
VERSION = 1

BOARD = 0
BCM = 1

IN = 0
OUT = 1

HIGH = True
LOW = False

PUD_DOWN = 0
PUD_UP = 1
PUD_OFF = -1

FALLING = 0
RISING = 1
BOTH = 2

_setup_mode = BOARD
_warnings = False

def setmode(mode):
    _setup_mode = mode

def setwarnings(mode):
    _warnings = mode

def setup(pin, mode, initial=None, pull_up_down=None):
    pass

def gpio_function(pin):
    return None

def cleanup(pin=None):
    pass

def output(pin, state):
    return LOW

def input(pin):
    return HIGH

def PWM(pin, frequency):
    return None

def wait_for_edge(pin, edge_type):
    pass

def add_event_detect(pin, edge_type, callback=None, bouncetime=0):
    pass

def add_event_callback(pin, callback, bouncetime=0):
    pass

def remove_event_detect(pin):
    pass

