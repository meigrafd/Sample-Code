<?php
if (!isset($_SESSION)) { session_start(); }
ini_set("session.gc_maxlifetime", 3600); // default: 3600 sec, 60 min

$impulsBlocktime = 20; // sec

ob_implicit_flush(true);
@ob_end_flush();

if (isset($_GET['Befehl']) AND $_GET['Befehl'] === 'impulsein') {
    if (isset($_SESSION['lastImpuls'])) {
        if ((time() - $_SESSION['lastImpuls']) > $impulsBlocktime) {
            sendImpuls();
        }
    } else {
            sendImpuls();
    }
}

function sendImpuls() {
    exec("/usr/local/bin/gpio -g write 23 1", $output, $return_var);
    sleep(1);
    exec("/usr/local/bin/gpio -g write 23 0", $output, $return_var);
    $_SESSION['lastImpuls'] = time();

    if (isset($return_var) AND $return_var == "126") { echo "<b>ERROR: Command found but not executable (Permission problem)!</b><br/>\n"; }
    if (isset($return_var) AND $return_var == "127") { echo "<b>ERROR: Command not found (Possible problem with PATH or a typo)!</b><br/>\n"; }
    if (isset($output) AND !empty($output)) {
        foreach ($output AS $line) {
            echo "$line<br/>\n";
        }
    }
}
?>

<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
<title>iframe.php</title>
<style>
  body {background-color:#DCDCDC;}
</style>
</head>

<body>
<p>
  <a href="?Befehl=impulsein"><img src="schranke-hoch.png" height="200" width="200" style="border:none;"></a>
</p>
</body>
</html>