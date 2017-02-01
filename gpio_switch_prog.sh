#!/bin/bash

# config - start
#
GPIOpin=17
Programm1=/bin/who
Programm2=/bin/last
#
# config - end

#function to get gpio pin value
function GetGPIOpinValue() {
	Value=-1; PIN=$1
	if [ -f "/sys/class/gpio/gpio${PIN}/value" ]; then
		Value=$(cat /sys/class/gpio/gpio${PIN}/value)
	fi
	echo $Value
}

#function to kill programm
function KillProg() {
	PID=$(cat /var/run/pid.$1)
	kill -9 $PID >/dev/null 2>&1
	killall -9 $1 >/dev/null 2>&1
	rm -f /var/run/pid.$1
}

#enable gpio pin
echo $GPIOpin > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio$GPIOpin/direction

#run Programm1
echo "starting Programm1"
$Programm1 &
#save pid from Programm1
echo $! > /var/run/pid.Programm1

#wait for $GPIOpin value to get 1
while :; do
	if [ "$(GetGPIOpinValue "$GPIOpin")" == 1 ]; then
		if [ -f "/var/run/pid.Programm1" ]; then
			echo "killing Programm1"
			KillProg "Programm1"
			echo "starting Programm2"
			#start Programm2
			$Programm2 &
			#save pid from Programm2
			echo $! > /var/run/pid.Programm2
		elif [ -f "/var/run/pid.Programm2" ]; then
			echo "killing Programm2"
			KillProg "Programm2"
			echo "starting Programm1"
			#start Programm1
			$Programm1 &
			#save pid from Programm1
			echo $! > /var/run/pid.Programm1
		fi
	fi
	sleep 1
done

