#!/bin/bash
#
# reset usb port of special usb-device
#
# http://raspberrypi.stackexchange.com/questions/6782/commands-to-simulate-removing-and-re-inserting-a-usb-peripheral
#
### CONFIG - START
SerialNumber="C6C3BACA"
### CONFIG - END

USBid=$(/bin/dmesg | grep $SerialNumber | tail -n1 | awk {'print $4'} | tr -d ":")
echo $USBid > /sys/bus/usb/drivers/usb/unbind
sleep 2
echo $USBid > /sys/bus/usb/drivers/usb/bind

echo "device re-mounted!"
