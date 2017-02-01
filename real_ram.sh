#!/bin/bash

[ -z $1 ] && echo "Usage: $0 <programm-name>" && exit 1

RealRAM=0
for PID in $(ps ux | grep -v grep | grep $1 | awk {'print $2'}); do
	RR=$(pmap -d $PID | grep "writeable/private:" | awk {'print $4'} | tr -d "K")
	[ -n "$RR" ] && RealRAM=$(( $RealRAM + $RR ))
done

echo "$1 real ram usage: $RealRAM kB = $(($RealRAM / 1024)) MB"

exit 0