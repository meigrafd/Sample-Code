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
import io
from datetime import datetime
from threading import Thread
from subprocess import Popen, PIPE

HOST = '0.0.0.0'  # 0.0.0.0 means all interfaces
PORT = 8000
RECORDTIME = 10  # seconds
RESOLUTION = (1024,768)
FRAMERATE = 24


class RaspiCamOutput(object):
    def __init__(self, camera):
        print 'Spawning background conversion process'
        self.converter = Popen([
            'avconv',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', '%dx%d' % camera.resolution,
            '-r', str(float(camera.framerate)),
            '-i', '-',
            '-f', 'h264',
            '-b', '800k',
            '-r', str(float(camera.framerate)),
            '-v', 'quiet',
            '-'],
            stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'), shell=False, close_fds=True)
    def write(self, b):
        self.converter.stdin.write(b)
    def flush(self):
        print 'Waiting for background conversion process to exit'
        self.converter.stdin.close()
        self.converter.wait()

class BroadcastThread(Thread):
    def __init__(self, converter, socket_client):
        super(BroadcastThread, self).__init__()
        self.converter = converter
        self.socket_client = socket_client
    def run(self):
        try:
            while True:
                buf = self.converter.stdout.read(1)
                if buf:
                    self.socket_client.send(buf)
                elif self.converter.poll() is not None:
                    break
        finally:
            self.converter.stdout.close()


def main():
    sockserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    try:
        sockserv.bind((HOST, PORT))
    except socket.error, msg:
        print 'Socket Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
        sys.exit()
    sockserv.listen(1)
    print 'Socket now listening.'
    try:
        print 'Initializing RaspberryPi Camera'
        camera = picamera.PiCamera()
        camera.resolution = RESOLUTION
        camera.framerate = FRAMERATE
        camera.brightness = 50
        camera.contrast = 0
        camera.annotate_text = ' %s ' % datetime.now().strftime('%d %b %Y - %H:%M:%S')
        
        while True:
            print 'Waiting for connection'
            # wait to accept a connection - blocking call
            conn, addr = sockserv.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            
            print 'Initializing broadcast thread'
            output = RaspiCamOutput(camera)
            broadcast_thread = BroadcastThread(output.converter, conn)

            print 'Starting recording'
            camera.led = True
            camera.start_recording(output, format='yuv')

            print 'Starting broadcast thread'
            broadcast_thread.start()
            
            start = datetime.now()
            while (datetime.now() - start).seconds < RECORDTIME:
                camera.annotate_text = ' %s ' % datetime.now().strftime('%d %b %Y - %H:%M:%S')
                camera.wait_recording(0.5)

            print 'Recordtime is over'
            camera.stop_recording()
            print 'Waiting for broadcast thread to finish'
            broadcast_thread.join()

            try:
                print 'Closing connection'
                if camera: camera.led = False
                conn.close()
            except:
                pass
    except (KeyboardInterrupt, SystemExit):
        print 'Quit'
    except Exception, error:
        print "Error: " + str(error)
    finally:
        c = camera.close()
        c = sockserv.close()
        c = conn.close()


if __name__ == '__main__':
    main()