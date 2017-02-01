#!/bin/bash
#
# v0.1 (c) by meigrafd
#

function ltrim () { echo "$1" | sed -e "s/^ *//"; }
function rtrim () { echo "$1" | sed -e "s/ *$//"; }
function trim () { x="$(ltrim "$1")"; echo "$(rtrim "$x")"; }

function dmesgDate () {
	while read line; do
		local dTime=$(echo $line | awk -F']' {'print $1'} | tr -d '[' | sed -e 's/^ *//')
		local LINE=$(echo $line | cut -d']' -f2-)
		local now=$(date +%s)
		local Uptime=$(cat /proc/uptime | cut -d'.' -f1)
		local t_now=$(( $now - $Uptime ))
		local t_time=$(echo "scale=0; $t_now + $dTime" | bc -l)
		local dTime=$(date -d@$t_time +"%H:%M:%S %d.%m.%Y")
		echo $dTime ${LINE}
	done < <(/bin/dmesg)
}

dmesgDate