#! /bin/bash
#
# http://www.forum-raspberrypi.de/Thread-shellscript-schleife-in-einem-bash-skript-erstellen
#

binary=({0..1}{0..1}{0..1}{0..1}{0..1})
for ((i=0; i<=31; i++));do
        echo ${binary[$i]}
done