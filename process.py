#!/usr/bin/python
#
# apt-get update
# apt-get install build-essential python-dev python-pip
# pip install psutil
#
import psutil, time

DEBUG = True

def check_proc_running(procname):
	start_time = time.time()
	found = False
	for proc in psutil.process_iter():
		if proc.name() == procname:
			found = True
			break
	end_time = time.time()
	if DEBUG:
		print "'check_proc_running' Function took %.3f seconds" % (end_time - start_time)
	return found

def get_proc_infos(procname):
	if check_proc_running(procname):
		start_time = time.time()
		for proc in psutil.get_process_list():
			if proc.name() == procname:
				cpu_percent = proc.get_cpu_percent()
				mem_percent = proc.get_memory_percent()
				rss, vms = proc.get_memory_info()
				rss = str(rss)
				vms = str(vms)
				break
		end_time = time.time()
		if DEBUG:
			print "'get_proc_infos' Function took %.3f seconds" % (end_time - start_time)
		return (cpu_percent, mem_percent, vms, rss)
	else:
		return False

