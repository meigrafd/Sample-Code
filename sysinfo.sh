#!/bin/bash

print() {
    printf "%-25s: %s %s\n" "$1" "$2 $3" "$4"
}

cpu_frequency() {
    local governorCPU=$(</sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)
    local curCPU=$(</sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq)
    local minCPU=$(</sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq)
    local maxCPU=$(</sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq)
    
    local mhz=$(awk "BEGIN {printf \"%.2f\", $curCPU/1000}")
    print "CPU current Frequency" $mhz "MHz"
    
    local mhz=$(awk "BEGIN {printf \"%.2f\", $minCPU/1000}")
    print "CPU minimal Frequency" $mhz "MHz"
    
    local mhz=$(awk "BEGIN {printf \"%.2f\", $maxCPU/1000}")
    print "CPU maximal Frequency" $mhz "MHz"
    
    print "CPU governor" $governorCPU ""
}

cpu_temperatur() {
    local cur=$(</sys/class/thermal/thermal_zone0/temp)
    local temp=$(awk "BEGIN {printf \"%.2f\", $cur/1000}")
    print "CPU current Temperature" $temp "°C"
}

system_memory() {
    local RAMtotal=$(grep ^MemTotal /proc/meminfo | awk {'print $2'})
    local MEMfree=$(grep ^MemFree /proc/meminfo | awk {'print $2'})
    local RAMbuffers=$(grep ^Buffers /proc/meminfo | awk {'print $2'})
    local RAMCached=$(grep ^Cached /proc/meminfo | awk {'print $2'})
    
    local RAMtotal=$(awk "BEGIN {printf \"%.2f\", $RAMtotal/1024}")
    local RAMfree=$(awk "BEGIN {printf \"%.2f\", ($MEMfree + $RAMbuffers + $RAMCached)/1024}")
    local RAMfreePerc=$(awk "BEGIN {printf \"%.2f\", ($RAMfree * 100)/$RAMtotal}")
    local RAMused=$(awk "BEGIN {printf \"%.2f\", ($RAMtotal - $RAMfree)}")
    local RAMusedPerc=$(awk "BEGIN {printf \"%.2f\", ($RAMused * 100) / $RAMtotal}")
    
    print "RAM Total" $RAMtotal "MB"
    print "RAM Used" $RAMused "MB"
    print "RAM Used Percent" $RAMusedPerc "%"
    print "RAM Free" $RAMfree "MB"
    print "RAM Free Percent" $RAMfreePerc "%"
}


echo
cpu_frequency
cpu_temperatur
echo
system_memory
echo

exit 0