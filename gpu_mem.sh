#!/bin/bash

LD_LIBRARY_PATH=/opt/vc/lib

TTOTALgpuMEM=$(/opt/vc/bin/vcgencmd get_mem gpu | awk -F'=' {'print $2'} | tr -d M)
TOTALgpuMEM=$(/opt/vc/bin/vcdbg reloc | grep total | awk {'print $5'} | tr -d M | tr -d ,)
FREEgpuMEM=$(/opt/vc/bin/vcdbg reloc | grep free | tail -n1 | awk {'print $3'} | tr -d M)
OFFLINEgpuMEM=$(/opt/vc/bin/vcdbg reloc | grep offline | tail -n1 | awk {'print $3'} | tr -d M)

MSG="GPU Memory free: ${FREEgpuMEM}MB"
[ -n "$OFFLINEgpuMEM" ]&&[ "$OFFLINEgpuMEM" != "allocated" ] && MSG="$MSG (${OFFLINEgpuMEM}MB offline)"
MSG="$MSG of ${TOTALgpuMEM}MB total (normaly total: ${TTOTALgpuMEM}MB)"

echo $MSG
