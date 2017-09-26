<!DOCTYPE html>
<html>
<head>
<title>MEM Watch</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<body>
<?php
$bashscript = "/usr/bin/memwatch.sh";

readBash();

echo "<h1>Memory Usage is ";
if (led_is_on($green)) {
    echo "OK";
} elseif (led_is_on($yellow)) {
    echo "Low";
} elseif (led_is_on($red)) {
    echo "Critical";
} else {
    echo "Unknown";
}
echo ".</h1>";

function led_is_on($number) {
    $status = 0;
    if (file_exists("/sys/class/gpio/gpio".$number."")) {
        $status = trim(file_get_contents("/sys/class/gpio/gpio".$number."/value"));
    }
    if ($status == "0") {
        return False;
    } else {
        return True;
    }
}

// Auslesen des memwatch.sh
// nur variablen in " " werden ausgelesen
function readBash() {
    global $bashscript;
    $bash=fopen("$bashscript","r");
    while($input = fgets($bash, 1024)) {
        preg_match("/^(.+)=\"(.*)\"/",trim($input),$find);
        if (isset($find[1]) AND !empty($find[1])) {
            if (!preg_match("/^\[|^.+\[\".+\"\]/",trim($find[1]))) {
                global $$find[1];
                if (empty($find[2])) { $find[2]='""'; }
                $$find[1] = $find[2];
            }
        }
    }
    @fclose($bash);
}
?>
</body>
</html>