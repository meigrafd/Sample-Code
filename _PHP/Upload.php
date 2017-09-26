<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<style>
 body {
  background-color:#0f1113;
 }
 .tab {
  letter-spacing: 0px;
  font-family: verdana, arial, helvetica, verdana, tahoma, sans-serif;
  font-size: 13px;
  text-align: left;
  color: #c8c8c8;
  font-weight: normal;
 }
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
</style>
</head>
<body>
<?php

# CONFIG - START

// Upload to which Directory?
$TMPdir="/tmp/upload";

# CONFIG - END

error_reporting(E_ALL);
ini_set("upload_max_filesize", "100M");
ini_set('track_errors', 1);
ini_set('display_errors', 1);
ini_set('log_errors', 1);

$s="&#160;";
$_SELF=$_SERVER['PHP_SELF'];
$UploadedFile = isset($_FILES["uploadfile"]) ? $_FILES["uploadfile"] : "";

echo "<form enctype='multipart/form-data' action='".htmlspecialchars($_SELF)."' method='POST'>\n";
echo "<b class='tab'>Datei:</b> <input name='uploadfile' type='file' size='50' maxlength='100000'>\n";
echo "$s$s<input type='submit' value='Upload'><br/><br/>\n";
echo "</form>\n";

if (!empty($UploadedFile)){
	if (!is_dir("$TMPdir") AND !mkdir("$TMPdir",0777,true)) {
		echo "<b class='tabred'>Error creating temp dir $TMPdir</b><br/>\n";
	} else {
		$FileName = $UploadedFile['name'];
		$FileError = $UploadedFile['error'];
		#exec("rm -rf ".$TMPdir."/* 2>/dev/null",$output,$return_var);
		if (!move_uploaded_file($UploadedFile['tmp_name'],"$TMPdir/".$FileName."")) {
			echo "<b class='tabred'>Beim Upload trat ein Fehler auf, bitte noch mal probieren!</b> \n";
			if (isset($FileError) AND !empty($FileError)) { echo "<b class='tab'>".uploaderror($FileError)."</b>"; }
			echo "<br/>\n";
		} else {
			$FileSize = get_size($UploadedFile['size']);
			$FileType = $UploadedFile['type'];
			echo "<b class='tabgreen'>Die Datei</b> <b class='tab'>".$FileName." (".$FileSize.")</b>";
			echo "<b class='tabgreen'>wurde erfolgreich hochgeladen und befindet sich nun in</b> <b class='tab'>".$TMPdir."</b><br/>\n";
		}
	}
}


function get_size($size,$precision=2,$long_name=true,$real_size=true) {
   $base=$real_size?1024:1000;
   $pos=0;
   while ($size>$base) {
      $size/=$base;
      $pos++;
   }
   $prefix=get_size_prefix($pos);
   $size_name=$long_name?$prefix."bytes":$prefix[0].'B';
   return round($size,$precision).' '.ucfirst($size_name);
}

function get_size_prefix($pos) {
   switch ($pos) {
      case 00: return "";
      case 01: return "Kilo";
      case 02: return "Mega";
      case 03: return "Giga";
      case 04: return "Tera";
      case 05: return "Peta";
      case 06: return "Exa";
      case 07: return "Zetta";
      case 08: return "Yotta";
      case 09: return "Xenna";
      case 10: return "W-";
      case 11: return "Vendeka";
      case 12: return "u-";
      default: return "?-";
   }
}

# http://www.php.net/manual/en/features.file-upload.errors.php
function uploaderror($returncode) {
	$msg="";
	switch ($returncode) {
		case 0:
			$msg = "";
			break;
		case 1:
			$msg = "The uploaded file exceeds the upload_max_filesize directive in php.ini.";
			break;
		case 2:
			$msg = "The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form.";
			break;
		case 3:
			$msg = "The uploaded file was only partially uploaded.";
			break;
		case 4:
			$msg = "No file was uploaded.";
			break;
		case 6:
			$msg = "Missing a temporary folder.";
			break;
		case 7:
			$msg = "Failed to write file to disk.";
			break;
		case 8:
			$msg = "A PHP extension stopped the file upload. PHP does not provide a way to ascertain which extension caused the file upload to stop";
			$msg.= " examining the list of loaded extensions with phpinfo() may help.";
			break;
		default:
			$msg = "Unknown upload error";
			break; 
	}
	return $msg;
}

?>

</body>
</html>
