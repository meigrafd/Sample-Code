#!/usr/bin/python3
# -*- coding: utf-8 -*-
# (c) 2018 by meigrafd
#
import sys
import time
import multiprocessing as mp
from datetime import datetime
from RPi import GPIO


class Sonar_Ranger:
    """
    This class encapsulates a type of acoustic ranger.  In particular
    the type of ranger with separate trigger and echo pins.
    
    A pulse on the trigger initiates the sonar ping and shortly
    afterwards a sonar pulse is transmitted and the echo pin
    goes high.  The echo pins stays high until a sonar echo is
    received (or the response times-out).  The time between
    the high and low edges indicates the sonar round trip time.
    """
    def __init__(self, gpio, trigger, echo, telemetry, status, settings, average=False, range_min=2, range_max=600):
        self.gpio = gpio
        self.trig = trigger
        self.echo = echo
        self.telemetry = telemetry
        self.status = status
        self.settings = settings
        self.average = average
        self.range_min = range_min
        self.range_max = range_max
        self.gpio.setup(self.trig, self.gpio.OUT)
        self.gpio.setup(self.echo, self.gpio.IN)
        self.start_time = time.time()
        self.gpio.add_event_detect(self.echo, self.gpio.BOTH, self.callback)
    
    def callback(self, channel):
        if self.gpio.input(self.echo) == 1:
            self.start_time = time.time()
        else:
            self.end_time = time.time()
            self.time_elapsed = self.end_time - self.start_time
            self.distance = self.time_elapsed / 0.000058
            self.telemetry['distance'] = self.distance
    
    def measure_average(self, count=3):
        c=1
        distance=0
        while (c <= count):
            self.ping()
            time.sleep(0.040)
            if self.distance:
                distance = distance + self.distance
                time.sleep(0.05)
                c+=1
        self.distance = distance/count
    
    def ping(self, pulse=0.00005):
        self.start_time=time.time()
        self.end_time=time.time()
        self.distance=None
        self.gpio.output(self.trig, self.gpio.HIGH)
        time.sleep(pulse)
        self.gpio.output(self.trig, self.gpio.LOW)
    
    def print_distance(self):
        if self.distance:
            if (int(time.time()) - self.status['announce_time']) >= self.settings['distance_announce_time']:
                if self.distance > self.range_max or self.distance < self.range_min:
                    print('Distance: out of range %.2f' % self.distance)
                else:
                    print('Distance: %.2f cm' % self.distance)
                self.status['announce_time'] = int(time.time())
    
    def run(self):
        while True:
            time.sleep(self.settings['distance_measure_time'])
            if not self.status['stop_ping']:
                if self.average:
                    self.measure_average()
                else:
                    self.ping()


class Motor_Control:
    """
    http://www.14core.com/wiring-driving-the-l298n-h-bridge-on-2-to-4-dc-motors/
    """
    def __init__(self, gpio, status, telemetry, motor_a_in1, motor_a_in2, motor_b_in3, motor_b_in4):
        self.gpio = gpio
        self.motor_a_in1 = motor_a_in1
        self.motor_a_in2 = motor_a_in2
        self.motor_b_in3 = motor_b_in3
        self.motor_b_in4 = motor_b_in4
        self.status = status
        self.telemetry = telemetry
        self.telemetry['steerTo']=0
        self.gpio.setup(self.motor_a_in1, self.gpio.OUT)
        self.gpio.setup(self.motor_a_in2, self.gpio.OUT)
        self.gpio.setup(self.motor_b_in3, self.gpio.OUT)
        self.gpio.setup(self.motor_b_in4, self.gpio.OUT)
    
    def stop(self):
        self.gpio.output(self.motor_a_in1, False)
        self.gpio.output(self.motor_a_in2, False)
        self.gpio.output(self.motor_b_in3, False)
        self.gpio.output(self.motor_b_in4, False)
        self.telemetry['steerTo'] = 'stop'
        print('Motor: {}'.format(self.telemetry['steerTo']))
    
    def forward(self):
        self.gpio.output(self.motor_a_in1, True)
        self.gpio.output(self.motor_a_in2, False)
        self.gpio.output(self.motor_b_in3, True)
        self.gpio.output(self.motor_b_in4, False)
        self.telemetry['steerTo'] = 'forward'
        print('Motor: {}'.format(self.telemetry['steerTo']))
    
    def reverse(self):
        self.gpio.output(self.motor_a_in1, False)
        self.gpio.output(self.motor_a_in2, True)
        self.gpio.output(self.motor_b_in3, False)
        self.gpio.output(self.motor_b_in4, True)
        self.telemetry['steerTo'] = 'reverse'
        print('Motor: {}'.format(self.telemetry['steerTo']))
    
    def turn_left(self):
        self.gpio.output(self.motor_a_in1, True)
        self.gpio.output(self.motor_a_in2, False)
        self.gpio.output(self.motor_b_in3, False)
        self.gpio.output(self.motor_b_in4, True)
        self.telemetry['steerTo'] = 'left'
        print('Motor: {}'.format(self.telemetry['steerTo']))
    
    def turn_right(self):
        self.gpio.output(self.motor_a_in1, False)
        self.gpio.output(self.motor_a_in2, True)
        self.gpio.output(self.motor_b_in3, True)
        self.gpio.output(self.motor_b_in4, False)
        self.telemetry['steerTo'] = 'right'
        print('Motor: {}'.format(self.telemetry['steerTo']))


def main():
    motor_a_in1 = 11
    motor_a_in2 = 7
    motor_b_in3 = 13
    motor_b_in4 = 15
    sonar_trigger = 38
    sonar_echo = 40
    GPIO.setmode(GPIO.BOARD)
    status = mp.Manager().dict()  # shared dictionary
    telemetry = mp.Manager().dict()  # shared dictionary
    settings=dict()  # static dictionary
    settings['distance_measure_time'] = 0.5  # sec
    settings['distance_announce_time'] = 1   # sec
    status['stop_ping']=False
    status['announce_time']=int(time.time())
    telemetry['distance']=None
    try:
        motor = Motor_Control(GPIO, status, telemetry, motor_a_in1, motor_a_in2, motor_b_in3, motor_b_in4)
        radar = Sonar_Ranger(GPIO, sonar_trigger, sonar_echo, telemetry, status, settings)
        # Spawn child process for running measurement
        radarProcess = mp.Process(target=radar.run)
        radarProcess.daemon = True
        radarProcess.start()
        time.sleep(1)
        while True:
            radar.print_distance()
            ## ..robots brain..
            
            if telemetry['distance'] and telemetry['distance'] < 15:
                if not telemetry['steerTo'] == 'left':
                    motor.turn_left()
            else:
                if not telemetry['steerTo'] == 'forward':
                    motor.forward()
            
            time.sleep(0.01)  # lowers CPU usage
    except (KeyboardInterrupt, SystemExit):
        if radarProcess.is_alive(): radarProcess.terminate()
        GPIO.cleanup()
            

if __name__ == '__main__':
    main()
