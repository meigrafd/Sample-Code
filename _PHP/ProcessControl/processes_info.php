<?php

CheckProcesses();
Process_Uptime();

echo "<div id='processes'>\n";
echo "<form name='control' action='".$_SERVER['PHP_SELF']."' method='POST'>\n";
echo "<table>\n";
foreach ($ProcRUN AS $Proc => $pid) {
	echo "<tr>\n";
	echo "<td><button type='submit' value='Start ".$Proc."' name='Control' class='Start'>Start</button>&nbsp;</td>\n";
	echo "<td><button type='submit' value='Stop ".$Proc."' name='Control' class='Stop'>Stop</button>&nbsp;</td>\n";
	echo "<td><button type='submit' value='Restart ".$Proc."' name='Control' class='Restart'>Restart</button>&nbsp;</td>\n";
	if ($pid <> "") {
		echo "<td class='tabgreen'>$Proc</td>";
		if (isset($ProcessUptime[$Proc])) {
			echo "<td>&nbsp; uptime: ".$ProcessUptime[$Proc]."</td>";
		} else {
			echo "<td>&nbsp; - </td>";
		}
	} else {
		echo "<td class='tabred'>$Proc</td>";
		echo "<td>&nbsp; - </td>";
	}
	echo "\n</tr>\n";
}
echo "</table>\n";
echo "</form>\n";
// Processes div - end
echo "</div>\n";


if (isset($_GET["UPDATE"])) { unset($_GET["UPDATE"]); }

//------------------------------------------------------------------------------

// Processes
function CheckProcesses() {
	global $Programms,$ProcRUN;
	$ProcRUN=array();
	//$ProcRUN["Cron"]=exec("ps aux | grep -v grep | grep -w cron | awk {'print $2'}");
	$PA=explode(" ", $Programms);
	foreach($PA AS $Prog) {
		$ProcRUN["$Prog"]=exec("ps aux | grep -v grep | grep -w ".basename($Prog)." | tail -n1 | awk {'print $2'}");
	}
}

// Process's Uptime
function Process_Uptime() {
	global $ProcRUN,$ProcessUptime;
	$ProcessUptime=array();
	foreach ($ProcRUN AS $Proc => $pid) {
		if ($Proc == "Cron") { continue; }
		if ($pid <> "") {
			$HZ=100;
			$p_seconds_since_boot = exec("cat /proc/".$pid."/stat 2>/dev/null|cut -d ' ' -f 22");
			$p_seconds_since_boot = intval($p_seconds_since_boot / $HZ);
			$boottime = exec("grep btime /proc/stat|cut -d ' ' -f 2");
			$p_starttime = intval($boottime + $p_seconds_since_boot);
			$now = time();
			$p_runtime = intval($now - $p_starttime);
			$ProcessUptime["$Proc"] = "".format_uptime($p_runtime)."";
		}
	}
}

// format the uptime in case the browser doesn't support dhtml/javascript
// static uptime string
function format_uptime($seconds) {
  $uptimeString="";
  $secs = intval($seconds % 60);
  $mins = intval($seconds / 60 % 60);
  $hours = intval($seconds / 3600 % 24);
  $days = intval($seconds / 86400);
  if ($days > 0) {
    $uptimeString .= $days;
    $uptimeString .= (($days == 1) ? " day" : " days");
  }
  if ($hours > 0) {
    $uptimeString .= (($days > 0) ? ", " : "") . $hours;
    $uptimeString .= (($hours == 1) ? " hour" : " hours");
  }
  if ($mins > 0) {
    $uptimeString .= (($days > 0 || $hours > 0) ? ", " : "") . $mins;
    $uptimeString .= (($mins == 1) ? " minute" : " minutes");
  }
  if ($secs > 0) {
    $uptimeString .= (($days > 0 || $hours > 0 || $mins > 0) ? ", " : "") . $secs;
    $uptimeString .= (($secs == 1) ? " second" : " seconds");
  }
  return $uptimeString;
}

?>