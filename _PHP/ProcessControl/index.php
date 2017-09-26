<?php
//------------------------------------------------------------------------------
$Programms = "Hamachi Mumble"; // exact Name of Processes without Path! Separate list with SPACE
$DIVUPDATES['processes'] = "10000";
$SudoWebScript = "/var/sudowebscript.sh";
//------------------------------------------------------------------------------
?>
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		<meta name="robots" content="DISALLOW">
		<title>Process Control</title>
		<style>
		.tabred {
			letter-spacing: 0px;
			font-family: verdana, arial, helvetica, verdana, tahoma, sans-serif;
			font-size: 13px;
			text-align: left;
			color: firebrick;
			font-weight: bold;
		}
		.tabgreen {
			letter-spacing: 0px;
			font-family: verdana, arial, helvetica, verdana, tahoma, sans-serif;
			font-size: 13px;
			text-align: left;
			color: limegreen;
			font-weight: bold;
		}
		.tab {
			letter-spacing: 0px;
			font-family: verdana, arial, helvetica, verdana, tahoma, sans-serif;
			font-size: 13px;
			text-align: left;
			color: #c8c8c8;
			font-weight: normal;
		}
		.Start { background-color:limegreen; color:black; }
		.Stop { background-color:firebrick; color:black; }
		.Restart { background-color:darkorange; color:black; }
		</style>
		<!-- Processes - auto refresh -->
		<script type="text/javascript">
			function getHTTPObject() {
				var http = false;
				// Use IEs ActiveX items to load the file.
				// MS Internet Explorer (ab v6)
				if(typeof ActiveXObject != "undefined") {
					try {http = new ActiveXObject("MSXML2.XMLHTTP");}
					catch (e) {
						// MS Internet Explorer (ab v5)
						try {http = new ActiveXObject("Microsoft.XMLHTTP");}
						catch (E) {http = false;}
					}
				// If ActiveX is not available, use the XMLHttpRequest of Firefox/Mozilla etc. to load the document.
				// Mozilla, Opera, Safari sowie Internet Explorer (ab v7)
				} else if (XMLHttpRequest) {
					try {http = new XMLHttpRequest();}
					catch (e) {http = false;}
				}
				return http;
			}
		
			var http = getHTTPObject();
			var ID = "processes";
			var url = "processes_info.php";
			var params = "UPDATE";
			var updatetime = "<?php echo $DIVUPDATES['processes'] ?>";
		
			//Call a function when the state changes.
			function handler() {
				if (http.readyState == 4 && http.status == 200) {
					document.getElementById(ID).innerHTML = http.responseText;
					// JavaScript function calls AutoRefresh() every .. seconds
					setTimeout("AutoRefresh()",updatetime);
				}
			}
			function AutoRefresh(){
				http.open("GET",url+"?"+params,true);
				http.onreadystatechange = handler;
				http.send(null);
			}
			AutoRefresh();
		</script>
	</head>
	<body>
<?php
if (!empty($_POST)) {
	foreach ($_POST AS $arg => $var) {
		if ($arg == "Control") {
			if (strpos($var, "Start") !== false) {
				$tmp = explode(" ", strtolower($var));
				exec('sudo '.$SudoWebScript.' start '.$tmp[1].'', $output, $return_var);
			}
			if (strpos($var, "Stop") !== false) {
				$tmp = explode(" ", strtolower($var));
				exec('sudo '.$SudoWebScript.' stop '.$tmp[1].'', $output, $return_var);
			}
			if (strpos($var, "Restart") !== false) {
				$tmp = explode(" ", strtolower($var));
				exec('sudo '.$SudoWebScript.' restart '.$tmp[1].'', $output, $return_var);
			}
		}
		if ($var == "Reboot Server") {
			echo "<br/><b style='font-weight:bold;color:#ffffff;font-size:15px;'>The system is going down for reboot NOW!</b><br/>";
			sleep(1);
			exec('sudo '.$SudoWebScript.' reb', $output, $return_var);
		}
	}
}

# Error/Output Handling
if (isset($return_var) AND $return_var >= 1) {
	echo "<font face='Arial, Helvetica, sans-serif' size='3' color='FF0000'>ERROR: </font>\n";
	echo "<font face='Arial, Helvetica, sans-serif' size='3' color='009900'>".exitcode($return_var)."<br/>\n";
}
if (isset($output) AND !empty($output)) {
	foreach($output AS $line) { echo $line."<br/>\n"; }
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
		<div id='control'>
			<?php include_once("processes_info.php"); ?>
		</div>
	</body>
</html>