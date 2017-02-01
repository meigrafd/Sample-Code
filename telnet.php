<?php
function telnet($host, $port, $command) {
    $socket = fsockopen($host, $port, $errno, $errstr);
    if ($socket) {
        echo "Connected\n";
    } else {
        echo "Connection failed: $errstr\n";
        return false;
    }
    fputs($socket, $command."\r\n");
    $buffer = "";
    while(!feof($socket)) {
        $buffer .= fgets($socket, 4096);
    }
    fclose($socket);
    return $buffer;
}

echo telnet("localhost", 23, "help");
?>