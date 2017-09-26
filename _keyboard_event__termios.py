#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# http://wiki.roxxs.org/index.php/Python/keyboard_event
# http://www.forum-raspberrypi.de/Thread-tutorial-direkte-tastaturabfrage-mit-python
#
from __future__ import print_function
import sys
import threading
import tty, termios
from time import sleep
if sys.version_info.major < 3:
    from Queue import Queue
else:
    from queue import Queue


def inkey(cq):
    while True:
        fd = sys.stdin.fileno()
        remember_attributes = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        character = sys.stdin.read(1) # wir lesen nur einzelne zeichen
        termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
        cq.put(character)
        if character == 'q' or character == '\x1b':  # x1b is ESC
            break


def main():
    char_queue = Queue()
    inkey_thread = threading.Thread(target=inkey, args=(char_queue,))
    inkey_thread.start()
    while True:
        if not char_queue.empty():
            char = char_queue.get()
            try:
                print("Key pressed is: %s" % char.decode('utf-8'))
            except (AttributeError, UnicodeDecodeError):
                print("character can not be decoded, sorry!")
            
            if char == 'q' or char == '\x1b':  # x1b is ESC
                break
        
        print("Program is running")
        sleep(1)


if __name__ == "__main__":
    main()
    print("\nQuit\n")

#EOF