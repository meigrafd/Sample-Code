<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width" />
<meta charset="UTF-8">
<title>Jutil Pi</title>
</head>
<body bgcolor="#82FA58">
<div align="center">

<b><span style="font-size:1.2em">JUTIL Pi</span></b>

<br/>
<br/>
<b>Beleuchtung</b>
<br/>
<br/>
<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
  <input type="submit" value="Ein" name="Beleuchtung" style="height: 50px; width: 75px;">
  <b>. . .</b> 
  <input type="submit" value="Aus" name="Beleuchtung" style="height: 50px; width: 75px;">
</form>
<br/>


<b>Fernseher</b>
<br/>
<br/>
<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
  <input type="submit" value="Ein" name="TV" style="height: 50px; width: 75px;">
  <b>. . .</b>  
  <input type="submit" value="Aus" name="TV" style="height: 50px; width: 75px;">
</form>
<br/>


<b>Alle</b>
<br/>
<br/>
<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
  <input type="submit" value="Ein" name="Alles" style="height: 50px; width: 75px;">
  <b>. . .</b>             
  <input type="submit" value="Aus" name="Alles" style="height: 50px; width: 75px;">
</form>
<br/>

<?php
if (!empty($_POST)) {
    foreach ($_POST AS $arg => $var) {
        if ($arg == "Beleuchtung") {
            if ($var == "Ein") {
                exec("sudo /home/pi/raspberry-remote/send 11010 1 1", $output, $return_var);
            } else if ($var == "Aus") {
                exec("sudo /home/pi/raspberry-remote/send 11010 1 0", $output, $return_var);
            }
        }
        else if ($arg == "TV") {
            if ($var == "Ein") {
                exec("sudo /home/pi/raspberry-remote/send 11010 2 1", $output, $return_var);
                exec("sudo /home/pi/raspberry-remote/send 11010 3 1", $output, $return_var);
            } else if ($var == "Aus") {
                exec("sudo /home/pi/raspberry-remote/send 11010 2 0", $output, $return_var);
                exec("sudo /home/pi/raspberry-remote/send 11010 3 0", $output, $return_var);
            }
        }
        else if ($arg == "Alles") {
            if ($var == "Ein") {
                exec("sudo /home/pi/raspberry-remote/send 11010 1 1", $output, $return_var);
                exec("sudo /home/pi/raspberry-remote/send 11010 2 1", $output, $return_var);
                exec("sudo /home/pi/raspberry-remote/send 11010 3 1", $output, $return_var);
            } else if ($var == "Aus") {
                exec("sudo /home/pi/raspberry-remote/send 11010 1 0", $output, $return_var);
                exec("sudo /home/pi/raspberry-remote/send 11010 2 0", $output, $return_var);
                exec("sudo /home/pi/raspberry-remote/send 11010 3 0", $output, $return_var);
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

</div>
</body>
</html>