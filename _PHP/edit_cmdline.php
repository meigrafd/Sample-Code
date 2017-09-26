<?php
ini_set("memory_limit","64M");
ini_set("max_execution_time","30");
ob_implicit_flush(true);
@ob_end_flush();
$_SELF=$_SERVER['PHP_SELF'];
$SPACERred=" <font color='#800000' class='trenn'>&#8226;</font> ";
$SPACERgreen=" <font color='green' class='trenn'>&#8226;</font> ";
$S="&nbsp;";
$s="&#160;";

//------------------------------------------------------------------------------
$eFILE['SYSTEM']['cmdline.txt']				= "/boot/cmdline.txt";
$eFILE['SYSTEM']['config.txt']				= "/boot/config.txt";
//------------------------------------------------------------------------------
# default language (currently only "ger")
$DEFlang="ger";
//------------------------------------------------------------------------------
# Sprach-Einstellungen
# Deutsch/German
$lang['ger']['title']					= 'Editor';
$lang['ger']['loadfile']			= 'Datei laden:';
$lang['ger']['welcome']				= '### Willkommen ###';
$lang['ger']['name_file']			= 'Verzeichnis:';
$lang['ger']['send_button']		= 'Speichern';
$lang['ger']['reset_button']	= 'Zur&uuml;cksetzen';
$lang['ger']['success']				= 'Erfolgreich gespeichert!';
$lang['ger']['not_writable']	= 'Kein Schreibrecht!';
$lang['ger']['no_file']				= 'Datei konnte nicht gefunden werden!';
$lang['ger']['no_save']				= 'Datei konnte nicht gespeichert werden!';
//------------------------------------------------------------------------------

?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="de">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<meta name="robots" content="disallow">
<style>
* { padding:0; margin:0; font-family:Verdana,Arial,sans-serif; }
body {
	background-repeat:no-repeat;
	background-position:50% 50%;
	background-attachment:fixed;
	background-color:#0f1113;
	font-size:86%;
	padding:10px;
	background-color:#0F1113;
	color:#6c6c6c;
}
#left { float:left; }
textarea {
	overflow:auto;
	resize:both;
	width:90%;
	margin:0px auto;
	padding:3px 0 0 3px;
	border:1px solid #6c6c6c;
	background-color:#0F1113;
	font-size:100%;
	color:#fff;
}
#content {
	position:absolute;
	width:87%;
	height:400px;
	top:58px;
	left:152px;
}
p.success { color: #FFD700; font-weight:bold; padding:5px 0 0 0; }
</style>
</head>
<body>

<?php
if (isset($_POST['Save'])) {
	$data_textlines = $_POST['textlines'];
	$data_repl = str_replace("\\", "", $data_textlines);
	$FileMatch=0;
	foreach ($eFILE as $TYPE => $E) {
		foreach ($E AS $FILENAME => $FILEPATH) {
			if ($_SERVER['QUERY_STRING'] == "${FILEPATH}"){
				$file=$FILEPATH;
				$FileMatch=1;
			}
		}
	}
	if (file_exists($file)){ unlink($file); }
	if (isset($file) AND !empty($file)) {
		$savedSUCCESS=1;
		if (!$file_handle = fopen($file,"w+")) {
			$savedSUCCESS=0;
			$NOTiCE.="<font color='#b22222'>".$lang["$DEFlang"]['not_writable']."</font><br/>\n";
		}
		if (!fwrite($file_handle, $data_repl)) {
			$savedSUCCESS=0;
			$NOTiCE.="<font color='#b22222'>".$lang["$DEFlang"]['no_save']."</font><br/>\n";
		}
	}
	fclose($file_handle);
	if (isset($savedSUCCESS) AND $savedSUCCESS == "1"){
		$NOTiCE.="<font color='#32cd32'>".$lang["$DEFlang"]['success']."</font><br/>\n";
	}
}

//------------------------------------------------------------------------------

echo "<div id='left' style='clear:right;'>\n";
echo " <form name='form1' method='POST' action='".$_SELF."?".$_SERVER['QUERY_STRING']."'>\n";
foreach ($eFILE AS $TYPE => $E) {
	if ($TYPE === "SYSTEM") {
		$FILEShtml["$TYPE"]=" <hr/>".$S."<font face='Georgia' size='2' color=FF0000>".$TYPE.":</b></font>\n";
	}
	$FILEShtml["$TYPE"].=" <div id='".$TYPE."'>\n";
	foreach ($E AS $FILENAME => $FILEPATH) {
		if ($TYPE === "SYSTEM") {
			_FS("$TYPE","$FILENAME");
			$FILEShtml["$TYPE"].="  <hr/>".$FSPACER."<a class='editor' href='".$_SELF."?".$FILEPATH."'>"._FileOpened($FILENAME,$FILEPATH)."</a>\n";
		}
	}
	$FILEShtml["$TYPE"].=" </div>\n";
}
foreach ($FILEShtml AS $TYPE => $code) { echo "$FILEShtml[$TYPE]\n"; }

echo " <hr/><br/><hr/><center><input style='width:130px; color:#211267; background-color:#2A972A; font-weight:bold;' type='reset' name='Submit' value='".$lang["$DEFlang"]['reset_button']."'/></center>\n";
echo " <hr/><center><input style='width:130px; color:#00FF00; background-color:#DD0505; font-weight:bold;' type='submit' name='Save' value='".$lang["$DEFlang"]['send_button']."'/><hr/></center>\n";
echo "</div>\n";
echo "<div id='content'>\n";
if (!$_SERVER['QUERY_STRING']) {
	echo " <textarea class='textarea' name='textlines' style='background-color:transparent' cols='110' rows='35' wrap='off' readonly>\n" ;
} else {
	#if (isset($_SERVER['QUERY_STRING']) && !isset($_POST['Save'])) { echo basename($_SERVER['QUERY_STRING'])."<br/>"; }
	echo " <textarea class='textarea' name='textlines' style='background-color:transparent' cols='110' rows='35' wrap='off'>\n" ;
}
$getFile='';
if (isset($_SERVER['QUERY_STRING']) AND !empty($_SERVER['QUERY_STRING'])) {
	$FileMatch=0;
	foreach ($eFILE as $TYPE => $E) {
		foreach ($E AS $FILENAME => $FILEPATH) {
			if ($_SERVER['QUERY_STRING'] == "$FILEPATH") {
				$getFile=$FILEPATH;
				$FileMatch=1;
			}
		}
	}	
	if ($FileMatch == "0" AND (isset($savedSUCCESS) AND $savedSUCCESS != "1")) {
		echo "".$lang["$DEFlang"]['no_file']."\n";
	}
} else { $NOTiCE.="".$lang["$DEFlang"]['welcome']."\n"; }
#if (!empty($getFile)) { GetcfgLines($getFile); }
if (!empty($getFile)) { echo file_get_contents($getFile); }

echo " </textarea>\n";
echo " </form>\n";
echo "</div>\n";
echo "<div id='NOTiCE' style='position:absolute; top:15px; left:160px;'>$NOTiCE</div>\n";


//------------------------------------------------------------------------------

function GetcfgLines($File) {
	$file = file("$File");
	for($i=0; $i<count($file); $i++) {
		$zeile = trim("$file[$i]");
		echo "".$zeile."\n";
	}
}

function _FS($TYPE,$file) {
	global $eFILE, $FSPACER, $SPACERgreen, $SPACERred;
	if (file_exists($eFILE[$TYPE][$file])) { $FSPACER=$SPACERgreen; } else { $FSPACER=$SPACERred; }
}

function _FileOpened($file,$filepath) {
	if (isset($_SERVER['QUERY_STRING']) AND !empty($_SERVER['QUERY_STRING'])) {
		if ($_SERVER['QUERY_STRING'] == "$filepath") {
			return "<font color='#ffd700'>$file</font>";
		} else {
			return "$file";
		}
	}
}

?>
</body>
</html>