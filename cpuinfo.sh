#!/bin/bash
export LD_LIBRARY_PATH=/opt/vc/lib
VCGENCMD=/opt/vc/bin/vcgencmd

CPUfreq=$(${VCGENCMD} measure_clock arm)
COREfreq=$(${VCGENCMD} measure_clock core)
COREvolt=$(${VCGENCMD} measure_volts core | awk -F'=' {'print $2'})
RAMvoltCORE=$(${VCGENCMD} measure_volts sdram_c | awk -F'=' {'print $2'})
RAMvoltIO=$(${VCGENCMD} measure_volts sdram_i | awk -F'=' {'print $2'})
RAMvoltPHY=$(${VCGENCMD} measure_volts sdram_p | awk -F'=' {'print $2'})

CPUfreq=$(echo "scale=2; $(echo $CPUfreq | awk -F'=' {'print $2'}) / 1000000" | bc -l)
COREfreq=$(echo "scale=2; $(echo $COREfreq | awk -F'=' {'print $2'}) / 1000000" | bc -l)
CPUtemp=$(echo "scale=2; $(cat /sys/class/thermal/thermal_zone0/temp | awk -F ' ' {'print $1'}) / 1000" | bc -l)

RAMtotal=$(grep ^MemTotal /proc/meminfo | awk {'print $2'})
MEMfree=$(grep ^MemFree /proc/meminfo | awk {'print $2'})
RAMbuffers=$(grep ^Buffers /proc/meminfo | awk {'print $2'})
RAMCached=$(grep ^Cached /proc/meminfo | awk {'print $2'})

RAMtotal=$(echo "scale=2; $RAMtotal / 1024" | bc -l)
RAMfree=$(echo "scale=2; ($MEMfree + $RAMbuffers + $RAMCached) / 1024" | bc -l)
RAMfreePerc=$(echo "scale=2; ($RAMfree * 100) / $RAMtotal" | bc -l)
RAMused=$(echo "scale=2; $RAMtotal - $RAMfree" | bc -l)
RAMusedPerc=$(echo "scale=2; ($RAMused * 100) / $RAMtotal" | bc -l)

echo 
echo "CPU current Frequency..: $CPUfreq MHz"
echo "CORE current Frequency.: $COREfreq MHz"
echo "CORE current Voltage...: $COREvolt"
echo "SD-RAM CORE  Voltage...: $RAMvoltCORE"
echo "SD-RAM IO    Voltage...: $RAMvoltIO"
echo "SD-RAM PHY   Voltage...: $RAMvoltPHY"
echo "CPU current Temperature: $CPUtemp °C"
echo
echo "RAM Total..............: $RAMtotal MB"
echo "RAM Used...............: $RAMused MB"
echo "RAM Used Percent.......: $RAMusedPerc %"
echo "RAM Free...............: $RAMfree MB"
echo "RAM Free Percent.......: $RAMfreePerc %"
echo

#echo "CODECS:"
#${VCGENCMD} codec_enabled H264
#${VCGENCMD} codec_enabled MPG2
#${VCGENCMD} codec_enabled WVC1
#echo