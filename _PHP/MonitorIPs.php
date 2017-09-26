#!/usr/bin/php
<?php
// v0.1
//----------------------------------------
$DBfile="/var/db.sqlite";
$DBtable="monitor";
$timeout = 1; # Timeout for Ping. Lower then 1 = BAD; Higher then 5 = BAD
//----------------------------------------
error_reporting(1);
set_time_limit(0);
@ob_implicit_flush(true);
@ob_end_flush();
//----------------------------------------

// check if sqlite db file exists else create it..
if (!file_exists($DBfile)) {
	$db = db_con($DBfile);
	$SQL ="CREATE TABLE IF NOT EXISTS ".$DBtable." (id INTEGER PRIMARY KEY,ip TEXT,online INT,datetime INT)";
	$create = db_query($SQL);
} else {
	$STATUS="offline";
	// get Added Entries
	$db = db_con($DBfile);
	$query = $db->query("SELECT ip FROM ".$DBtable." WHERE 1");
	$DURATION_start = startTime();
	while ($result = $query->fetch(PDO::FETCH_ASSOC)) {
		$id = $result['id'];
		$IP = $result['ip'];
		print "Checking IP: ".(gethostbyname($IP))."";
		$IP2 = prepare_host($IP);
		if (preg_match("/:(.*)/",$IP2,$match)) { $PORT = $match[1]; }
		if (empty($PORT)) { $PORT = 80; }
		$OnlineCheck = @fsockopen($IP2, $PORT, $errno, $errstr, $timeout);
		if ($OnlineCheck) {
			$STATUS = "Online";
			$DATETIME = time();
			$update = db_query("UPDATE ".$DBtable." SET datetime='".$DATETIME."',online='1' WHERE ip='".$IP."'");
		} else {
			// offline
			$update = db_query("UPDATE ".$DBtable." SET online='0' WHERE ip='".$IP."'");
		}
		@fclose($OnlineCheck);
		print " -> $STATUS\n";
	}
	echo "\ncheck took ".endTime($DURATION_start)." seconds\n\n";
}

function prepare_host($IP) {
	$IP = preg_replace("/https?:\/\//i","",$IP);
	$IP = preg_replace("/(.+?)(\/.+$)/i","$1",$IP);
	return $IP;
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

//______________________________________________________________________________________
// sqlite

// DB connect
function db_con($DBfile) {
	if (!$db = new PDO("sqlite:$DBfile")) {
		$e="font-size:23px; text-align:left; color:firebrick; font-weight:bold;";
		echo "<b style='".$e."'>Fehler beim öffnen der Datenbank: $DBfile</b><br/>";
		echo "<b style='".$e."'>".$db->errorInfo()."</b><br/>";
		die;
	}
	$db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	return $db;
}

// DB Query..
function db_query($sql) {
	global $DBfile,$db;
	if (!isset($db) OR empty($db)) { $db = db_con($DBfile); }
	$result = $db->query($sql) OR db_error($sql,$db->errorInfo());
	return $result;
}

//Function to handle database errors
function db_error($sql,$error) {
	die('<small><font color="#ff0000"><b>[DB ERROR]</b></font></small><br/><br/><font color="#800000"><b>'.$error.'</b><br/><br/>'.$sql.'</font>');
}

?>