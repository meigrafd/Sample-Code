#!/bin/bash

[ -z "$1" ] && echo "Usage: $0 <max-temp>" && exit 1

[ ! -x /usr/bin/bc ] && [ "$(whoami)" == "root" ] && apt-get install bc


CPUtemp=$(echo "scale=1; $(cat /sys/class/thermal/thermal_zone0/temp | awk -F ' ' {'print $1'}) / 1000" | bc -l)

if [ "$CPUtemp" -gt "$1" ]; then
	echo "CPU Temp $CPUtemp is too high!"
fi

exit 0