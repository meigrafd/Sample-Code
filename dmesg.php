#!/usr/bin/php
<?php
// v0.1
error_reporting(0);
set_time_limit(0);
@ob_implicit_flush(true);
@ob_end_flush();
//$S="&nbsp;";
$S=" ";

$lines = file("/var/log/dmesg");
for ($i=0; $i<count($lines); $i++) {
    $zeile = trim($lines[$i]);
    $EndTpos1=(strpos($zeile, "]") - 1);
    $EndTpos2=(strpos($zeile, "]") + 1);
    $TIME=trim(substr($zeile, 1, $EndTpos1));
    $TIME=date("H:i:s d.m.Y", dmesgTime($TIME));
    $LINE=substr("$zeile", $EndTpos2);
    printf("$line %s", "[".$TIME."]  ".str_replace(" ", $S, $LINE)."\n");
}

function dmesgTime($time) {
    global $Uptime;
    $now = time();
    if (!isset($Uptime)) { $Uptime = shell_exec("cat /proc/uptime | cut -d'.' -f1"); }
    $t_now = $now - $Uptime;
    $t_time = $t_now + $time;
    return $t_time;
}
?>
