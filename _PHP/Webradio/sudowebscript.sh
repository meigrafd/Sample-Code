#!/bin/bash
#
# sudo web script allowing user www-data to run commands with root privilegs
#
# www-data ALL=NOPASSWD:/var/sudowebscript.sh
#

case "$1" in
	control) mpc $2 ;;
	sender) mpc $2 ;;
	*) echo "ERROR: invalid parameter: $1 (for $0)"; exit 1 ;;
esac

exit 0