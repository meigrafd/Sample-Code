#!/usr/bin/env python
# coding: utf8
from __future__ import absolute_import, division, print_function
import Tkinter as tk
from datetime import datetime as DateTime, timedelta as TimeDelta
from itertools import count
from RPi import GPIO

START_PIN = 22
LOG_FILENAME = 'log.txt'


class Stopwatch(object):
    def __init__(self, log_filename):
        self.log_filename = log_filename
        self.part_counter = count()
        self.start_time = None
        self._elapsed_time = TimeDelta()
    
    def __str__(self):
        minutes, seconds = divmod(self.elapsed_time.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        return '{0:02d}:{1:02d}:{2:02d}'.format(hours, minutes, seconds)
    
    @property
    def is_running(self):
        return self.start_time is not None
    
    @property
    def elapsed_time(self):
        if self.is_running:
            return DateTime.now() - self.start_time
        else:
            return self._elapsed_time
    
    def start(self):
        if not self.is_running:
            self.start_time = DateTime.now()
    
    def stop(self):
        if self.is_running:
            self._elapsed_time = self.elapsed_time
            self.start_time = None
            with open(self.log_filename, 'a') as log_file:
                log_file.write(
                    'Teil #{0} {1}\n'.format(next(self.part_counter), self)
                )


class StopwatchUI(tk.Frame):
    def __init__(self, parent, stopwatch):
        tk.Frame.__init__(self, parent)
        self.stopwatch = stopwatch
        self.time_label = tk.Label(parent, font=('Helvetica', 150))
        self.time_label.pack()
        tk.Button(parent, text='Start', command=self.stopwatch.start).pack()
        tk.Button(parent, text='Stop', command=self.stopwatch.stop).pack()
        tk.Button(parent, text='Quit', command=self.quit).pack()
        self._update_display()
    
    def _update_display(self):
        self.time_label['text'] = str(self.stopwatch)
        self.after(10, self._update_display)


def main():
    try:    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        root = tk.Tk()
        root.overrideredirect(True)
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry('{0}x{1}+0+0'.format(width, height))
        root.wm_title('Stoppuhr')
        stopwatch = Stopwatch(LOG_FILENAME)
        GPIO.add_event_detect(START_PIN, GPIO.FALLING, stopwatch.start)
        stopwatch_ui = StopwatchUI(root, stopwatch)
        stopwatch_ui.pack()
        root.mainloop()
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()

#EOF