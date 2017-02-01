<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>1 wire</title>
  </head>
  <body>
<?php
    // (c) meigrafd 09.2015
    // http://www.forum-raspberrypi.de/Thread-raspbian-temperaturlogging-webserver-problem-cronjob?pid=183371#pid183371
    if (!file_exists("/sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count")) {
        echo "<b>ERROR: w1 Kernel Module not loaded?<br/>modprobe w1-gpio pullup=1<br/>modprobe w1-therm<br/></b>\n";
    } else if (file_get_contents("/sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count") === 0) {
        echo "<b>ERROR: No 1-wire Sensors connected?</b>\n";
    } else {
        $w1_slaves = file("/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves");
        foreach ($w1_slaves AS $slave) {
            $lines = file("/sys/bus/w1/devices/".$slave."/w1_slave");
            if (preg_match("/t=(.*)/", $lines[1], $match)) {
                echo $slave.": ".$match[1]."<br/>\n";
            }
        }
    }
?>
  </body>
</html>