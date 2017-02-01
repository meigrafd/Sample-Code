<?php

$DBfile = "/var/sqlite.db";
$TABLE="sysinfos";

#-------------------------------------------------------------------
error_reporting(E_ALL);
ini_set('track_errors', 1);
ini_set('display_errors', 1);
ini_set('log_errors', 1);
$ERROR='';
#-------------------------------------------------------------------

$show = isset($_GET["show"]) ? $_GET["show"] : "";
$time = isset($_GET["time"]) ? $_GET["time"] : "";
$wert = isset($_GET["wert"]) ? $_GET["wert"] : "";
$was = isset($_GET["was"]) ? $_GET["was"] : "";

if (isset($_GET["debug"])) { $DEBUG = $_GET["debug"]; unset($_GET["debug"]); }
if (isset($DEBUG) AND $DEBUG == 1) { showarray($_GET); }

// check if sqlite db file exists else create it..
if (!file_exists($DBfile)) {
	$SQL = "CREATE TABLE IF NOT EXISTS ".$TABLE." (id TEXT PRIMARY KEY,datetime INT,was TEXT,wert TEXT)";
	$db = db_con($DBfile);
	$create = db_query($SQL);
}

if (!empty($wert)) {
	if (empty($was)) { $ERROR.="- ?was Fehlt! \n"; }
	if (empty($ERROR)) {
		if (empty($time)) { $time=time(); }
		$SQL ="INSERT INTO ".$TABLE." (datetime,was,wert) VALUES ('".$time."','".$was."','".$wert."')";
		$db = db_con($DBfile);
		$insert = db_query($SQL);
	}
}
if (!empty($show)) {
	$db = db_con($DBfile);
	$query = db_query("SELECT * FROM ".$TABLE." WHERE 1 ORDER BY datetime DESC");
	while($result = $query->fetch(PDO::FETCH_ASSOC)){
		$id = $result['id'];
		$datetime = date('d.m.Y H:i:s',$result['datetime']);
		$WAS = $result['was'];
		$WERT = $result['wert'];
		echo "[".$datetime."] $WAS: $WERT<br/>\n";
	}
}

if (!empty($ERROR)) {
	echo "Error: \n";
	echo "$ERROR\n";
}

#--- functions

// DB connect
function db_con($DB) {
	if (!$db = new PDO("sqlite:$DB")) {
		$e="font-size:23px; text-align:left; color:firebrick; font-weight:bold;";
		echo "<b style='".$e."'>Fehler beim öffnen der Datenbank $DB:</b><br/>";
		echo "<b style='".$e."'>".$db->errorInfo()."</b><br/>";
		die;
	}
	$db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	return $db;
}

// DB Query
function db_query($sql) {
	global $db;
	$result = $db->query($sql) OR db_error($sql,$db->errorInfo());
	return $result;
}

// DB errors
function db_error($sql,$error) {
	die('<small><font color="#ff0000"><b>[DB ERROR]</b></font></small><br/><br/><font color="#800000"><b>'.$error.'</b><br/><br/>'.$sql.'</font>');
}

// Add HTML character incoding to strings
function db_output($string) {
	return htmlspecialchars($string);
}
// Add slashes to incoming data
function db_input($string) {
	if (function_exists('mysql_real_escape_string')) {
		return mysql_real_escape_string($string);
	}
	return addslashes($string);
}

//______________________________________________________________________________________
// debug

function showarray($array) {
	echo "<pre><b style='font-size:13px; text-align:left; color:#c8c8c8;'>\n";
	var_dump($array);
	echo "</b>\n";
	flush();
}
?>