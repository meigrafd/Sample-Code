#!/bin/bash
#
# Code to disable RaspberryPI LAN-Chip to save ~100mA.
#
#Aber das bringt glaub ich nicht so viel da er dann weiterhin bischen Strom zieht.. das reduziert den Strombedarf nur um ca. 100mA
#und wie gesagt würden die USB-Ports dann auch nicht mehr funktionieren da beim Modell-B die R36 und R37 Überbrückung (0 ohm) fehlt
#
# more on:
# http://www.element14.com/community/thread/18844
# http://www.forum-raspberrypi.de/Thread-usb-ports-deaktivieren?pid=220954#pid220954
#

#Code to stop
/etc/init.d/networking stop
echo 0 > /sys/devices/platform/bcm2708_usb/buspower;
echo "Bus power stopping"

#Code to start
echo 1 > /sys/devices/platform/bcm2708_usb/buspower;
echo "Bus power starting"
sleep 2;
/etc/init.d/networking start


## Since Kernel 4.x:

#Code to stop
/etc/init.d/networking stop
echo 0 > /sys/devices/platform/soc/*.usb/buspower
echo "Bus power stopping"

#Code to start
echo 1 > /sys/devices/platform/soc/*.usb/buspower
echo "Bus power starting"
sleep 2
/etc/init.d/networking start

# another methode: http://stackoverflow.com/questions/1163824/linux-usb-turning-the-power-on-and-off
echo 0 > /sys/bus/usb/devices/geräteid/authorized
echo 1 > /sys/bus/usb/devices/geräteid/authorized