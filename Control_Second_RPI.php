<!DOCTYPE html>
<html>
  <head>
    <title>Control</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
  </head>
  <body>
<?php
// v0.1
$SecondRPIip = "192.168.0.50";
$ShutdownTimer = "2"; # in Minuten
#----------------------------------------------
$_SELF=$_SERVER['PHP_SELF'];
$PREcmd = 'bash ';
$WebScript = '/var/webscript.sh ';

$START = isset($_POST["START"]) ? $_POST["START"] : "";
$SHUTDOWN = isset($_POST["SHUTDOWN"]) ? $_POST["SHUTDOWN"] : "";

if (!empty($START)) { exec(''.$PREcmd.''.$WebScript.'start', $output, $return_var); }
if (!empty($SHUTDOWN)) { exec(''.$PREcmd.''.$WebScript.'stop', $output, $return_var); }

# Error/Output Handling
$out="";
if (isset($return_var) AND $return_var >= 1) {
	$out .= "ERROR: ". exitcode($return_var) ."<br/>\n";
}
if (isset($output) AND !empty($output)) {
	$status = "ERROR";
	foreach($output AS $line) { $out .= "$line<br/>\n"; }
	$out .= "<br/>".$out."<br/>";
} else {
	$status = "OK";
}
if ($status == "OK") { $fontcolor="009900"; }
if ($status == "ERROR") { $fontcolor="FF0000"; }
echo ("<font face='Arial, Helvetica, sans-serif' size='3' color='".$fontcolor."'>".$status."</font>".$out."\n");


echo "<table border=1 cellpadding=3 bordercolorlight>\n";
echo "<tr>\n";
echo "<td><form method='POST' id='Control' name='StartForm' action='".$_SELF."'>\n";
echo "<input type='hidden' name='START' value='START'>\n";
echo "<input id='StartButton' type='submit' value='Start Second Raspberry'></form></td>\n";
echo "<td><form method='POST' id='Control' name='StopForm' action='".$_SELF."'>\n";
echo "<input type='hidden' name='STOP' value='STOP'>\n";
echo "<input id='StopButton' type='submit' value='Shutdown Second Raspberry'></form></td>\n";
echo "</tr>\n";
echo "</table>\n";

// Function to handle $return_var (exit codes)
/*
   An exit status of zero indicates success. A non-zero exit status indicates failure. 
   When a command terminates on a fatal signal N, bash uses the value of 128+N as the exit status.

   If  a command is not found, the child process created to execute it returns a status of 127.  If a com-
   mand is found but is not executable, the return status is 126.

   If a command fails because of an error during expansion or redirection, the exit status is greater than
   zero.

   Shell  builtin  commands  return  a  status of 0 (true) if successful, and non-zero (false) if an error
   occurs while they execute.  All builtins return an exit status of 2 to indicate incorrect usage.

   Bash itself returns the exit status of the last command executed, unless  a  syntax  error  occurs,  in
   which case it exits with a non-zero value.
   
   source: http://tldp.org/LDP/abs/html/exitcodes.html
*/
function exitcode($code) {
	switch($code) {
		case 0: $Reason = "Successful"; break;
		case 1: $Reason = "General Error (Miscellaneous errors, such as 'divide by zero' and other impermissible operations)"; break;
		case 2: $Reason = "Incorrect Usage"; break;
		case 126: $Reason = "Command found but not executable (Permission problem)"; break;
		case 127: $Reason = "Command not found (Possible problem with \$PATH or a typo)"; break;
		case 128: $Reason = "Invalid argument to exit (exit takes only integer args in the range 0 - 255)"; break;
		#case 130: $ReturnCode = "Script terminated by Control-C"; break;
		default:
			# http://de.wikipedia.org/wiki/Signal_(Unix)
			$Signal = $code - 128;
			switch($Signal) {
				#case 0: $Reason = ""; break;
				case 1: $Reason = "Hangup detected on controlling terminal or death of controlling process"; break;
				case 2: $Reason = "Interrupt from keyboard; interactive attention signal. Script terminated by Control-C"; break;
				case 3: $Reason = "Quit from keyboard."; break;
				case 4: $Reason = "Illegal instruction."; break;
				case 5: $Reason = "Trace/breakpoint trap."; break;
				case 6: $Reason = "Abnormal termination; abort signal from abort(3)."; break;
				case 7: $Reason = "BUS error (bad memory access)."; break;
				case 8: $Reason = "'Floating-point exception': erroneous arithmetic operation."; break;
				case 9: $Reason = "Kill, unblockable."; break;
				case 10: $Reason = "User-defined signal 1."; break;
				case 11: $Reason = "'Segmentation violation': invalid memory reference."; break;
				default: $Reason = $code;
			}
	}
	return $Reason;
}

// Function to get realtime output of executed command
function _exec($cmd, $status="") {
	$fontcolour="ffffff";
	if ($status == "OK") { $fontcolour="009900"; }
	if ($status == "ERROR") { $fontcolour="FF0000"; }
	$handle = popen("$cmd 2>&1", 'rb');
	while (!feof($handle)) {
		$line = stream_get_line($handle, 10000, "\n");
		if (empty($line)) { continue; }
		if (preg_match("/^error/i", $line)) { $fontcolour="FF0000"; }
		$line = str_replace(" ", "&nbsp;", $line);
		echo ("<font face='Arial, Helvetica, sans-serif' size='2' color='".$fontcolour."'>".$line."</font><br/>\n");
		flush();
	}
	pclose($handle);
	return;
}

// Function to check response time
function pingDomain($domain){
	$starttime = microtime(true);
	$file      = fsockopen ($domain, 80, $errno, $errstr, 10);
	$stoptime  = microtime(true);
	$status    = 0;
	if (!$file) $status = -1;  // Site is down
	 else {
		fclose($file);
		$status = ($stoptime - $starttime) * 1000;
		$status = floor($status);
	}
	return $status;
}

function ping($host, $timeout = 1) {
	/* ICMP ping packet with a pre-calculated checksum */
	$package = "\x08\x00\x7d\x4b\x00\x00\x00\x00PingHost";
	#$socket  = socket_create(AF_INET, SOCK_RAW, 1);
	$socket  = socket_create(AF_UNIX, SOCK_STREAM, 0);
	socket_set_option($socket, SOL_SOCKET, SO_RCVTIMEO, array('sec' => $timeout, 'usec' => 0));
	socket_connect($socket, $host, null);
	$ts = microtime(true);
	socket_send($socket, $package, strLen($package), 0);
	if (socket_read($socket, 255)) {
		$result = microtime(true) - $ts;
	} else {
		$result = false;
	}
	socket_close($socket);
	return $result;
}
?>
  </body>
</html>
