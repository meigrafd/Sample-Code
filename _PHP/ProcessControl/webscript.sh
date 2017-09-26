#!/bin/bash
#
# sudo web script allowing user www-data to run commands with root privilegs
#
# visudo:
# www-data ALL=NOPASSWD:/var/sudowebscript.sh
#

ProgramBinPath=(
	'apache2::/etc/init.d/apache2'
	'oidentd::/etc/init.d/oidentd'
)

start_prog() {
	prog=$1
	PID="$(ps auxw | grep -v grep | grep -v $0 | grep $prog | awk {'print $2'})"
	if [[ ! -z $PID ]] ; then
		echo "$prog  ist bereits gestartet"
	else
		$(GetProgBinPath $prog) start &
		sleep 1
		PID="$(ps auxw | grep -v grep | grep -v $0 | grep $prog | awk {'print $2'})"
		if [[ -z $PID ]] ; then
			echo "$prog  konnte nicht gestartet werden!?"
		else
			echo "$prog  gestartet"
		fi
	fi
}

stop_prog() {
	prog=$1
	PID="$(ps auxw | grep -v grep | grep -v $0 | grep $prog | awk {'print $2'})"
	if [[ -z $PID ]] ; then
		echo "$prog  ist bereits beendet"
	else
		pkill -9 $prog >/dev/null 2>&1
		sleep 2
		PID="$(pgrep -x $prog)"
		if [[ ! -n $PID ]] ; then
			echo "$prog  beendet"
		else
			pkill -9 $prog
			echo "$prog  gekillt"
		fi
	fi
}

GetProgBinPath() {
	prog=$1
	for index in "${ProgramBinPath[@]}" ; do
		KEY="${index%%::*}"
		VALUE="${index##*::}"
		[[ "$KEY" == "$prog" ]] && echo "$VALUE" && break
	done
}

case "$1" in
	start)
		start_prog "$2"
	;;
	stop)
		stop_prog "$2"
	;;
	restart)
		stop_prog "$2"
		sleep 2
		start_prog "$2"
	;;
	reb) /sbin/shutdown -r now ;;
	*) echo "ERROR: invalid parameter: $1 (for $0)"; exit 1 ;;
esac

exit 0