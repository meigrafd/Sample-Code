#!/bin/bash
#
# http://www.forum-raspberrypi.de/Thread-raspbian-einfache-datei-mit-variablen-erstellen-und-auslesen?pid=144814#pid144814
#
# copy X to a file
X='
[mac_1]
user = login
pass = bla
ip = 192.168.0.10
path = /pfad/zum/script
exec = script1.scpt

[pi_1]
user = login1
pass = blub
ip = 192.168.0.20
path = /path/to/script
exec = script.sh

[pi_2]
user = login2
pass = ber
ip = 192.168.0.22
path = /path/to/script
exec = script.py

[pi_3]
user = "log in"
pass = blub ber
ip = 192.168.0.22
path = /path/to/script
narf = the brain!
';

INI=/path/to/file

function get_ini() {
	while IFS='^ = ' read variable value ; do
		if [[ $variable == \[*\] ]]; then
			local section=$(echo $variable | sed -e 's|\[||' -e 's|\]||')
		elif [[ $value ]]; then
			#echo "$variable[\"$section\"]=$value"
			declare -Ag "$variable[\"$section\"]=$value"
		fi
	done < $INI
}

get_ini
echo
echo ${user[pi_2]}

