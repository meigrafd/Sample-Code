#!/usr/bin/python2.7
#
# Copyright (C) 2016 by meiraspi@gmail.com published under the MIT License
#
# connect to stream using VLC over Networkstream address => tcp/h264://raspberrypi:8000
#
import socket
import picamera
import sys
import os
from datetime import datetime

HOST = '0.0.0.0'  # 0.0.0.0 means all interfaces
PORT = 8000
RECORDTIME = 10  # seconds


def picam_record(camera=None, Dest='/tmp/video.h264', Resolution=(1024,768), Format='h264', Recordtime=5, Quality=30, Framerate=24, Led=True):
    # check if "Dest" is an object or some type of file..
    DestTypeFile = isinstance(Dest, basestring) #if string = True, if object = False
    try:
        if camera == None: camera = picamera.PiCamera()
        print 'Starting record'
        camera.led = Led
        camera.resolution = Resolution
        camera.framerate = Framerate
        camera.start_preview()
        camera.annotate_text = ' %s ' % datetime.now().strftime('%d %b %Y - %H:%M:%S')
        start = datetime.now()
        camera.start_recording(Dest, format=Format, quality=Quality)
        while (datetime.now() - start).seconds < Recordtime:
            camera.annotate_text = ' %s ' % datetime.now().strftime('%d %b %Y - %H:%M:%S')
            camera.wait_recording(0.1)
        print 'Recordtime is over'
        camera.stop_recording()
        #camera.stop_preview()
        if DestTypeFile == True:
            print 'Captured %s' % Dest
            # rename file
            # get dirname and filename without extension
            dirName = os.path.dirname(Dest)
            fileName = os.path.basename(Dest)
            fileBasename = os.path.splitext(fileName)[0]
            fileExtension = os.path.splitext(fileName)[1]
            # rename file with timestamp
            newFile = dirName + '/' + fileBasename + '_' + datetime.now().strftime('%d%m%Y_%H%M%S') + fileExtension
            os.rename(Dest, newFile)
            print 'Renamed file to %s' % newFile
            if camera is not None: camera.close()
    except Exception, error:
        print "Error in 'picam_record': " + str(error)


def main():
    sockserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    try:
        sockserv.bind((HOST, PORT))
    except socket.error, msg:
        print 'Socket Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
        sys.exit()
    sockserv.listen(1)
    print 'Socket now listening'
    try:
        Cam = picamera.PiCamera()
        while True:
            # wait to accept a connection - blocking call
            conn, addr = sockserv.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            # make a file-like object out of the connection
            conn = conn.makefile('wb') 
            picam_record(camera=Cam, Dest=conn, Recordtime=RECORDTIME, Quality=20)
            try:
                print 'Closing connection'
                if Cam: Cam.led = False
                conn.close()
            except:
                pass
    except (KeyboardInterrupt, SystemExit):
        print 'Quit'
    except Exception, error:
        print "Error: " + str(error)
    finally:
        c = Cam.close()
        c = sockserv.close()
        c = conn.close()


if __name__ == '__main__':
    main()