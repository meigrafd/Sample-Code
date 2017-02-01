#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serial, time, sys
#-------------------------------------------------------------------

SerialPort = "/dev/ttyACM0"
SerialBaudrate = 38400

#-------------------------------------------------------------------

# serial docu: http://pyserial.sourceforge.net/pyserial.html

#-------------------------------------------------------------------

def ArduinoAuslesen(serObject):
    while True:
        try:
            # Remove newline character '\n'
            response = serObject.readline().strip()
            #response = serObject.readline()
            if response:
                print("Arduino-> "+str(response)),
                # ...do something with it...
        except serial.SerialException as e:
            print("Could not read serial port '{}': {}".format(SerialPort, e))
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
    serObject.close()

#-------------------------------------------------------------------

def main():
    #initialization and open the port.
    #possible timeout values:
    #   1. None: wait forever, block call
    #   2. 0: non-blocking mode, return immediately
    #   3. x, x is bigger than 0, float allowed, timeout block call
    ser = serial.Serial()
    ser.port = SerialPort
    ser.baudrate = SerialBaudrate
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
    try:
        ser.open()
    except Exception as e:
        print("Error open serial port: " + str(e))
        sys.exit()
    if ser.isOpen():
        try:
            ser.flushInput()    #flush input buffer, discarding all its contents
            ser.flushOutput()   #flush output buffer, aborting current output and discard all that is in buffer
            ArduinoAuslesen(ser)
        except Exception as e:
            print("Error...: " + str(e))
        except (KeyboardInterrupt, SystemExit):
            print("\nSchliesse Programm..\n")
            if ser: ser.close()
            sys.exit()

if __name__ == '__main__':
    main()