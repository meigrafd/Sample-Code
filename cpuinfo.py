#!/usr/bin/python
#
# Get CPU Info of RaspberrPi for only one core.
# (c) 10.2015 by meigrafd
#
from __future__ import print_function

def getCPUinfo():
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
    return info

if __name__ == '__main__':
    cpuInfo = getCPUinfo()[0]
    for name in cpuInfo:
        print("{0:16}: {1}" . format(name, cpuInfo[name]))

    #only print 'Serial' info:
    print(cpuInfo['Serial'])