#!/bin/bash
GPIO[1]="0 1 4 17 21 22 10 9 11 18 23 24 25 8 7"
GPIO[2]="2 3 4 17 27 22 10 9 11 18 23 24 25 8 7"

#get raspi revision
RaspiRev=$(gpio -v | grep "Revision" | awk {'print $5'} | tr -d ",")
[ -z "$RaspiRev" ] && echo 'Error getting Raspi Revision!' && exit 1
mkdir -p /tmp/sg

echo "Scanning..."

#create temp script for each gpio and run it in background
for gpio in ${GPIO[$RaspiRev]}; do
	echo "gpio -g wfi $gpio both" > /tmp/sg/$gpio
	echo "echo $gpio" >> /tmp/sg/$gpio
	bash /tmp/sg/$gpio &
done

#executed when this script exits. kill temp scripts and cleanup
function finish() {
	for pid in $(pidof gpio); do
		kill -9 $pid >/dev/null 2>&1
	done
	rm -rf /tmp/sg
}
trap finish EXIT

#hold script running until [Enter] is pressed
function pause() {
	echo -e 'Press [Enter] to quit\n'
	read -p "$*"
}
pause
exit 0