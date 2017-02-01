#!/usr/bin/php
<?php
// v0.1 by meigrafd
error_reporting(E_ALL);
set_time_limit(0);
@ob_implicit_flush(true);
@ob_end_flush();

$FoundFile = "/tmp/brute_FOUND.txt";

$charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
#$charset.= "ÖÄÜ";
#$charset.= strtolower($charset);
#$charset.= "ß";
$charset.= "0123456789";
#$charset.= '²³µ°~`!@#$%^&§*()|{}[]-_\\/\'";:,.+=<>? ';
$charset.= '-_';

if (empty($argv[1])) { print "Usage: scan <sub%.domain.com>\n"; exit(); }
$HOST = $argv[1];
preg_match("/(.*)%(.*)/",$HOST,$match);
if (empty($match[1])) { print "Missing needed search-tag % in domain!\n"; exit(); }
$Xcount = substr_count($HOST,"%");
$Xrepeat = str_repeat("%",$Xcount);
$HostSplit = explode($Xrepeat,$HOST);
$SubDomain = $HostSplit[0];
$Domain = $HostSplit[1];
$charset_length = strlen($charset);

$overall_DURATION_start = startTime();

recurse($Xcount,0,'');

function recurse($width, $position, $base_string) {
	global $charset, $charset_length, $DURATION_start, $overall_DURATION_start;
	for ($i = 0; $i < $charset_length; ++$i) {
		$DURATION_start = startTime();
		check($base_string . $charset[$i]);
		if ($position  < $width - 1) {
			recurse($width, $position + 1, $base_string . $charset[$i]);
		}
	}
	echo "overall scan took ".endTime($overall_DURATION_start)." seconds\n\n";
}

function check($string) {
	global $DURATION_start, $SubDomain, $Domain, $FoundFile;
	$string = trim("".$SubDomain."".$string."".$Domain."");
#	echo "checking $string ...\n";
	$IP = gethostbyname($string);
	if (!empty($IP) AND $IP !== $string) {
		echo "\nFOUND MATCH: ".$string."\r\n";
		echo "scan took ".endTime($DURATION_start)." seconds\n\n";
		WriteFound($FoundFile, "$string");
		#exit();
	}
}

function startTime() {
	$timeExplode = explode(" ", microtime());
	$time = $timeExplode[1] + $timeExplode[0];
	return $time;
}
function endTime($timer) {
	$timeExplode = explode(" ", microtime());
	$time = $timeExplode[1] + $timeExplode[0];
	$finish = $time - $timer;
	$endTime = sprintf("%4.3f", $finish); 
	return $endTime;
}

function WriteFound($filename, $line) {
	$handle = fopen($filename, "a");
	if ($handle) {
		fwrite($handle, "$line\n");
	}
	fclose($handle);
}

?>