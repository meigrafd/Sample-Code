#!/bin/bash

benchmark_filesize=100
benchmark_temp_file="$HOME/benchmark.file"

write_speed=$(dd bs=4K count=$(( $benchmark_filesize * 1024 / 4 )) if=/dev/zero of=$benchmark_temp_file conv=fdatasync 2>&1 | grep 'MB' | awk '{print $8, $9}')

#Clear cache
sync
echo 3 > /proc/sys/vm/drop_caches

read_speed=$(dd bs=4K count=$(( $benchmark_filesize * 1024 / 4 )) if=$benchmark_temp_file of=/dev/zero conv=fdatasync 2>&1 | grep 'MB' | awk '{print $8, $9}')

#Delete Test File
rm "$benchmark_temp_file" &> /dev/null

echo Write: $write_speed
echo Read: $read_speed


