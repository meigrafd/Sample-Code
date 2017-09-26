#!/usr/bin/php
<?php
// v0.2
//
// dd if=/dev/zero of=/benchmark bs=1M count=2
// dd if=/dev/sda of=/dev/null bs=1M count=1000
//
error_reporting(0);
set_time_limit(0);

if (empty($argv[1]) OR empty($argv[2])) { print "Usage: $argv[0] <Source> <Dest>\n"; exit(); }

$SourceFileSize = filesize($argv[1]);
print "Transfering ".$argv[1]." (".$SourceFileSize." Bytes) to ".$argv[2]."\n";

$DURATION_start=microtime(true);
exec("cp -rf ".$argv[1]." ".$argv[2]."");
$DURATION_end=microtime(true);
$DURATION = $DURATION_end - $DURATION_start;

print "took ".round($DURATION,3)." seconds\n";

$TransferSpeed = $SourceFileSize / $DURATION;
#print "~ ".round($TransferSpeed,3)." Byte/s";

$TransferSpeed = $TransferSpeed / 1024;
#print " ~ ".round($TransferSpeed,3)." kB/s";

$TransferSpeed = $TransferSpeed / 1024;
print " ~ ".round($TransferSpeed,3)." MB/s\n";
?>
