<?php

$GPIO_TUER = 0; // Tuer Oeffner Kontakt
$GPIO_BWM = 2;  // Bewegungsmelder im Windfang

$MAC['willi'] = '12:34:56:78:9A:BC';
$MAC['moni'] = '98:76:54:32:10:FE';

$HANDY['willi'] = 'Nexus';
$HANDY['moni'] = 'S3';


// Init GPIOs
if (!file_exists("/sys/class/gpio/gpio".$GPIO_TUER."")) {
    $success = file_put_contents("/sys/class/gpio/export", $GPIO_TUER);
    $success = file_put_contents("/sys/class/gpio/gpio".$GPIO_TUER."/direction", "out");
}
if (!file_exists("/sys/class/gpio/gpio".$GPIO_BWM."")) {
    $success = file_put_contents("/sys/class/gpio/export", $GPIO_BWM);
    $success = file_put_contents("/sys/class/gpio/gpio".$GPIO_BWM."/direction", "in");
}

function ping($mac, $handyType) {
    $response = trim(shell_exec("hcitool name $mac"));
    preg_match("/$handyType/", $response, $match);
    if (!empty($match[0])) { return true; }
    return false;
}

//Dauerschleife
while (1) { 
    //Wenn Bewegungsmelder im Windfang eine Bewegung erkannt hat
    if (trim(file_get_contents("/sys/class/gpio/gpio".$GPIO_BWM."/value")) == 1) {
        //Pruefen ob Handy pingbar
        foreach($MAC AS $PERSON => $ADDR) {
            if (ping($ADDR, $HANDY[$PERSON]) == true) {
                $success = file_put_contents("/sys/class/gpio/gpio".$GPIO_TUER."/value", 1);
                sleep(3);
                $success = file_put_contents("/sys/class/gpio/gpio".$GPIO_TUER."/value", 0);
            }
        }
    }
    //prevent high cpu usage..
    sleep(0.5);
}
?>