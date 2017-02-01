#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serial
import time
import sys
#-------------------------------------------------------------------
ser = serial.Serial()

ser.port = "/dev/ttyUSB0"
ser.baudrate = 38400
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None     #block read
ser.timeout = 1         #non-block read
#ser.timeout = 2        #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False      #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False      #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2    #timeout for write
#-------------------------------------------------------------------

try:
    ser.open()
except Exception as e:
    print("Error open serial port: " + str(e))
    sys.exit()
if ser.isOpen():
    try:
        while True:
            Eingabe = raw_input("Was soll gesendet werden? > ")
            if not Eingabe:
                print("Bitte irgend etwas eingeben!")
                continue
            response = None
            print("Sende: %s" % input)
            ser.write(Eingabe + "\n")
            while response is None:
                time.sleep(0.01)
                response = ser.readline().strip()
            print("Antwort: %s" % response)
    except Exception as e:
        print("Error...: " + str(e))
    except (KeyboardInterrupt, SystemExit):
        print("\nSchliesse Programm..\n")
        if ser: ser.close()