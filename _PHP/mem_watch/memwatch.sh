#!/bin/bash
# Dateiname: memwatch.sh

#GPIO Pins, können bei bedarf auch ruhig veraendert werden
green="17"
yellow="18"
red="4"

# Initialisiert die LEDs bei Start des Programms
init_leds() {
	for i in $green $yellow $red ; do
		[ ! -f /sys/class/gpio/gpio${i}/value ] && echo $i > /sys/class/gpio/export
		echo out > /sys/class/gpio/gpio${i}/direction
		echo 0 > /sys/class/gpio/gpio${i}/value
	done
}

# Schaltet die LED entspreched des Status
set_led() {
	init_leds
	echo 1 > /sys/class/gpio/gpio${1}/value
}

# Setzt alles zurück auf Originalzustand bei Programmende
cleanup() {
	for i in $green $yellow $red ; do
		[ -f /sys/class/gpio/gpio${i}/value ] && echo $i > /sys/class/gpio/unexport
	done
	exit 0
}

init_leds
trap cleanup INT TERM EXIT

# Analyse des RAM-Speichers und Schaltbefehl der entsprechenden LED geben
while :; do
	total=`free | grep Mem | awk {'print $2'}`
	memfree=`free | grep Mem | awk {'print $4'}`
	cachefree=`free | grep cache: | awk {'print $4'}`
	free=$(( memfree + cachefree ))
	available=$(( free * 100 / total ))
	echo -n "$available% of memory available -> "
	if [ "$available" -le 10 ]; then
		echo "Critical"
		set_led $red
	elif [ "$available" -le 30 ]; then
		echo "Low"
		set_led $yellow
	else
		echo "OK"
		set_led $green
	fi
	sleep 10
done