#!/usr/bin/python3
# coding: utf-8
#
# http://www.forum-raspberrypi.de/Thread-python-problem-mit-tkinter-subprocess-realtime-output
#
# 21.05.2016  Copyright (C) by meigrafd (meiraspi@gmail.com) published under the MIT License
#
import time
import shlex
import tkinter as tk
import psutil
from subprocess import Popen, PIPE
import multiprocessing
from queue import Empty as QueueEmpty


# http://stackoverflow.com/a/32682520
# http://stackoverflow.com/a/16989631
class cmdExe:
    def __init__(self, choices, debug=False):
        self.choices = choices
        self.DEBUG = debug
        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.build_widgets()
        self.master.eval('tk::PlaceWindow %s center' % self.master.winfo_pathname(self.master.winfo_id()))
        self.master.mainloop()

    def build_widgets(self):
        self.master.geometry("500x500+10+10")
        self.master.title("Command Executor")
        self.status_label = tk.Label(master=self.master)
        self.status_label.configure(text=" ", fg="red")
        self.status_label.grid(row=0, column=0, columnspan=4, sticky=tk.W)
        self.startstop_button = tk.Button(master=self.master, bg="#229", fg="white", text="Run", command=self.startstop_func)
        self.exit_button = tk.Button(master=self.master, bg="#229", fg="white", text="X", command=self.quit)
        self.running = tk.BooleanVar()
        self.running.set(False)
        self.process = None
        self.option_choice = tk.StringVar(self.master)
        self.option_choice.set(self.choices[0])
        self.options = tk.OptionMenu(self.master, self.option_choice, *self.choices)
        self.options.grid(row=1, column=0)
        self.options.config(font=('calibri',(10)), bg='white', width=12)
        self.options['menu'].config(font=('calibri',(10)), bg='white')
        self.entry = tk.Entry(master=self.master, width=20)
        self.entry.focus()
        self.entry.grid(row=1, column=1)
        self.startstop_button.grid(row=1, column=2)
        self.exit_button.grid(row=0, column=4, sticky=tk.E)
        self.Log = tk.Text(master=self.master, height=31, width=68)
        self.Log.grid(row=2, column=0, columnspan=5)
        self.ScrollLog = tk.Scrollbar(self.master)
        self.ScrollLog.grid(row=2, column=5, sticky=tk.NE + tk.SE)
        self.ScrollLog.configure(command=self.Log.yview)
        self.Log.configure(yscrollcommand=self.ScrollLog.set)
        self.message_queue = multiprocessing.Manager().Queue()
        self.master.after(100, self.CheckQueuePoll, self.message_queue)

    def CheckQueuePoll(self, m_queue):
        try:
            str = m_queue.get(0)
            self.Log.insert(tk.END, str)
        except QueueEmpty:
            pass
        finally:
            self.master.after(100, self.CheckQueuePoll, m_queue)

    # updates button states
    def update_all(self):
        button_list = {self.startstop_button}
        for b in button_list:
            b.update()

    def startstop_func(self):
        if self.process is None:
            if self.running.get() == True:
                self.printD("Error: only one running command at once allowed!")
                self.status_label.configure(text="Error: another command is active!", fg="red")
                return

            self.command = self.option_choice.get()
            if self.entry.get() is not None:
                self.command = self.command + " " + self.entry.get()
            self.printD("\nExecuting command: %s\n" % self.command)
            self.running.set(True)
            self.status_label.configure(text="..running..", fg="green")
            self.startstop_button["text"] = "Stop"

            self.returncode = self.execute_command(self.command)
            if (self.returncode is not None) and (self.returncode != 0):
                if self.DEBUG:
                    print("Returncode: ", end='')
                    print(self.returncode)
                self.status_label.configure(text="Error!", fg="red")
            else:
                self.status_label.configure(text="Done: "+self.command, fg="green")
        else:
            self.printD("Killing Process")
            self.process.kill()
            self.status_label.configure(text="Killed: "+self.command, fg="green")
        self.running.set(False)
        self.process = None
        self.startstop_button["text"] = "Run"


    def mp_execute(self, command):
        self.entry.delete(0, tk.END)
        self.Log.delete('1.0', tk.END)
        self.process = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, bufsize=1)
        for output in iter(self.process.stdout.readline, b''):
            self.writeLog(output)
            self.printD(output.strip())
        if self.process is not None:
            rc = self.process.poll()
            self.process.stdout.close()
            self.process.wait()
        self.printD("\nDone")
        return rc


    def execute_command(self, command):
        rc = -1
        self.entry.delete(0, tk.END)
        self.Log.delete('1.0', tk.END)
        self.process = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, bufsize=1)
        for output in iter(self.process.stdout.readline, b''):
            self.writeLog(output)
            self.printD(output.strip())
        if self.process is not None:
            rc = self.process.poll()
            self.process.stdout.close()
            self.process.wait()
        self.printD("\nDone")
        return rc

    def printD(self, text):
        if self.DEBUG:
            print(text)

    def writeLog(self, text):
        self.Log.insert(tk.END, (text))
        self.Log.see(tk.END)
        self.Log.update()

    def quit(self):
        if self.process is not None:
            try: self.process.kill() # exit subprocess if GUI is closed (zombie!)
            except: pass
        self.master.destroy()
        print("Quit")


#-------------------------------------------------------------------

if __name__ == '__main__':
    # selectable commands from dropdown menu
    choices = [
        'apt-get update',
        'apt-get upgrade -y',
        'apt-get install -y',
        'ls -la',
        'apt-get',
    ]
    try:
        tkinter_app = cmdExe(choices, True)
    except (KeyboardInterrupt, SystemExit):
        print("Schliesse Programm.")
