#!/usr/bin/python3
import sys
import io
import os
import picamera
from subprocess import Popen, PIPE
from time import sleep


###########################################
# CONFIGURATION
SERVER_URL = "rtmp://live.twitch.tv/app"
STREAM_KEY = "xxxxxxx"
BITRATE = "200k"
WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
###########################################


class BroadcastOutput(object):
    def __init__(self, camera, bitrate, url, key):
        print('Spawning background conversion process')
        self.converter = Popen([
            'avconv',
            '-f', 'rawvideo',
            '-pix_fmt', 'yuv420p',
            '-s', '%dx%d' % camera.resolution,
            '-r', str(float(camera.framerate)),
            '-i', '-',
            '-f', 'mpeg1video',
            '-b', str(bitrate),
            '-r', str(float(camera.framerate)),
            '%s/%s' % (url, key)],
            stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
            shell=False, close_fds=True)
    def write(self, b):
        self.converter.stdin.write(b)
    def flush(self):
        print('Waiting for background conversion process to exit')
        self.converter.stdin.close()
        self.converter.wait()

def main():
    print('Initializing camera')
    with picamera.PiCamera() as camera:
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMERATE
        sleep(1) # camera warm-up time
        print('Initializing twitch stream output')
        output = BroadcastOutput(camera, BITRATE, SERVER_URL, STREAM_KEY)
        print('Starting recording')
        camera.start_recording(output, 'yuv')
        try:
            while True:
                camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            print('Stopping recording')
            camera.stop_recording()

if __name__ == '__main__':
    main()
