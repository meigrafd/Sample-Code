#!/usr/bin/python
#
# Get CPU Info of RaspberrPi for only one core.
# (c) 10.2015 by meigrafd
#
from __future__ import print_function

def get_cpu_info():
    info = [{}]
    try:
        fo = open('/proc/cpuinfo')
    except EnvironmentError, e:
        print("Error:", str(e))
    else:
        for line in fo:
            name_value = [s.strip() for s in line.split(':', 1)]
            if len(name_value) != 2:
                continue
            name, value = name_value
            info[-1][name] = value
        fo.close()
    return info[0]

if __name__ == '__main__':
    cpu_info = get_cpu_info()
    for name in cpu_info:
        print("{0:16}: {1}" . format(name, cpu_info[name]))

    #only print 'Serial' info:
    print(cpu_info['Serial'])