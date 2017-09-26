<?php

/*
     index.html: http://pastebin.de/72155
     usermod -G gpio -a www-data
     /etc/init.d/apache2 restart
*/

function init_GPIO($pin, $direction) {
    $handle = @fopen("/sys/class/gpio/export", 'a');
    @fwrite($handle, $pin);
    @fclose($handle);
    $handle = @fopen("/sys/class/gpio/gpio".$pin."/direction", 'a');
    @fwrite($handle, $direction);
    @fclose($handle);
}

function einschalten($pin) {
    $handle = @fopen("/sys/class/gpio/gpio".$pin."/value", 'a');
    @fwrite($handle, "1");
    @fclose($handle);
}

function ausschalten($pin) {
    $handle = @fopen("/sys/class/gpio/gpio".$pin."/value", 'a');
    @fwrite($handle, "0");
    @fclose($handle);
}

function pinDirection($pin) {
   $Direction='';
   if (file_exists("/sys/class/gpio/gpio".$pin."")) {
       $Direction = trim(file_get_contents("/sys/class/gpio/gpio".$pin."/direction"));
   }
    return $Direction;
}

function pinValue($pin) {
   $Value='';
    if (file_exists("/sys/class/gpio/gpio".$pin."")) {
        $Value = trim(file_get_contents("/sys/class/gpio/gpio".$pin."/value"));
    }
   return $Value;
}


if (isset($_GET['mode']) && isset($_GET['pin'])) {

    $pin = $_GET['pin'];
    $mode = $_GET['mode'];

    if (strlen($pin) <= 2) {
        init_GPIO($pin, "out");
        if ($mode == "on") {
            einschalten($pin);
        } else {
            ausschalten($pin);
        }
        echo pinValue($pin);
    }
}
?>
