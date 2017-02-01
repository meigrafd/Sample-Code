#!/bin/bash
#
# Morse IP over RaspberryPI's OK led
#
# Usage: morse.sh 1.2.3.4
#

[ -z "$1" ] && echo "Usage: $(basename $0) 1.2.3.4" && exit 1

IP=$1
LED=/sys/class/leds/led0

# gap between number-blocks
dotDelay=4s
# gap between number-chars
numDelay=2s
# gap between on/off
oDelay=0.5s


# init led
echo none > $LED/trigger
sleep 2

# morse $IP, strip each .'s
for i in $(echo $IP | tr "." " "); do
	#echo "i:$i"
	# for each number-block
	for ii in $(echo "$i" | sed -e 's/\(.\)/\1\n/g'); do
		#echo "ii:$ii"
		# for each number-char
		for (( c=1; c<=$ii; c++ )); do
			#echo "c:$c"
			echo 1 > $LED/brightness
			sleep $oDelay
			echo 0 > $LED/brightness
			sleep $oDelay
		done
		sleep $numDelay
	done
	sleep $dotDelay
done

sleep 10
# init led to normal
echo mmc0 > $LED/trigger

exit 0