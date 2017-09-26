<?php

$SudoWebScript = '/var/sudowebscript.sh';

if (isset($_GET['cmd'])) {
	$command = $_GET['cmd'];
	if ($command == "current") {
		exec("mpc current", $output, $return_var);
	} elseif ($command == "volume") {
		exec("mpc volume", $output, $return_var);
	} elseif ($command == "leiser") {
		exec("mpc volume -5", $output, $return_var);
	} elseif ($command == "lauter") {
		exec("mpc volume +5", $output, $return_var);
	} elseif ($command == "stop") {
		exec("mpc stop", $output, $return_var);
	}
}
if (isset($_GET['sender'])) {
	$number = $_GET['sender'];
	exec("mpc play ".$number, $output, $return_var);
}

if (isset($return_var) AND $return_var >= 1) {
	echo "ERROR: <br/>";
	echo exitcode($return_var)."\n";
}
if (isset($output) AND !empty($output)) {
	foreach($output AS $line) { echo $line."<br/>\n"; }
}

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

?>