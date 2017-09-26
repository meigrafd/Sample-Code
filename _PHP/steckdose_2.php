<!DOCTYPE html>
<html>
  <head>
    <title>Funksteuerung</title>
  <style>
    input[type=submit] {
      padding:5px 15px;
      border:0 none;
      cursor:pointer;
      -webkit-border-radius: 5px;
      border-radius: 5px;
    }
  </style>
  </head>
  <body>

<?php

// http://www.forum-raspberrypi.de/Thread-andere-webinterface-fuehrt-nur-einen-befehle-aus?pid=217574#pid217574

if (!empty($_POST)) {
    foreach ($_POST AS $arg => $var) {
        if ($arg == "Alles") {
            if ($var == "An") {
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 1 1", $output, $return_var);
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 2 1", $output, $return_var);
            } else if ($var == "Aus") {
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 1 0", $output, $return_var);
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 2 0", $output, $return_var);
            }
        }
        else if ($arg == "Lampe1") {
            if ($var == "An") {
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 1 1", $output, $return_var);
            } else if ($var == "Aus") {
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 1 0", $output, $return_var);
            }
        }
        else if ($arg == "Deckenfluter1") {
            if ($var == "An") {
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 2 1", $output, $return_var);
            } else if ($var == "Aus") {
                exec("sudo /home/pi/433Utils/RPi_utils/send 11111 2 0", $output, $return_var);
            }
        }
    }

    if (isset($return_var) AND $return_var >= 1) {
        echo "ERROR: <br/>\n";
        echo exitcode($return_var)."<br/>\n";
    } else if (isset($output) AND !empty($output)) {
        foreach($output AS $line) { echo $line."<br/>\n"; }
    }
}
?>

<br/>

<form method="POST" action="<?php echo $_SERVER['PHP_SELF']; ?>">

  <b>Lampe 1</b><br/>
  <input type="submit" value="An" name="Lampe1">
  <b>. . .</b> 
  <input type="submit" value="Aus" name="Lampe1">
  <br/><br/>

  <b>Deckenfluter 1</b><br/>
  <input type="submit" value="An" name="Deckenfluter1">
  <b>. . .</b>  
  <input type="submit" value="Aus" name="Deckenfluter1">
  <br/><br/>

  <b>Alles</b><br/>
  <input type="submit" value="An" name="Alles">
  <b>. . .</b> 
  <input type="submit" value="Aus" name="Alles">

</form>

  </body>
</html>

<?php
function exitcode($code) {
    $ReturnCode['0'] = "Successful";
    $ReturnCode['1'] = "General Error (Miscellaneous errors, such as 'divide by zero' and other impermissible operations)";
    $ReturnCode['2'] = "Incorrect Usage";
    $ReturnCode['126'] = "Command found but not executable (Permission problem)";
    $ReturnCode['127'] = "Command not found (Possible problem with PATH or a typo)";
    $ReturnCode['128'] = "Invalid argument to exit (exit takes only integer args in the range 0 - 255)";
    $ReturnCode['130'] = "Script terminated by Control-C";
    return $ReturnCode[$code];
}
?>