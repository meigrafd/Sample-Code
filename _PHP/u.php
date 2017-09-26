<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<body>
<?php

$TMPdir="/tmp/upload";
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
		exec("rm -rf ".$TMPdir."/* 2>/dev/null",$output,$return_var);
		if (!move_uploaded_file($UploadedFile['tmp_name'],"$TMPdir/".$UploadedFile['name']."")) {
			echo "<b class='tabred'>Beim Upload trat ein Fehler auf, bitte noch mal probieren!</b><br/>\n";
		} else {
			$FileName = $UploadedFile['name'];
			$FileSize = get_size($UploadedFile['size']);
			$FileType = $UploadedFile['type'];
			echo "<b class='tabgreen'>Die Datei</b> <b class='tab'>".$FileName."</b> <b class='tabgreen'>wurde erfolgreich hochgeladen</b> <b class='tab'>(".$FileSize.")</b><br/>\n";
		}
		exec("cd ".$TMPdir." && tar -xz --file=".$UploadedFile['name']."",$output,$return_var);
		if ($return_var == "127") { echo "<p/><b>ERROR no such Script!</b><br/>\n"; $WORKS=0; }
		elseif (!empty($output)) { echo "<br/>\n"; foreach ($output as $value) { echo "<b class=tab>".$value."</b><br/>\n"; } }
		else { $WORKS=1; }
		if ($WORKS === 0) {
			echo "<br/><b>ERROR executing script!</b><br/>\n";
		} else {
			exec("cd ".$TMPdir."; rm -f ".$UploadedFile['name']."");
			$EF0 = glob("$TMPdir/*");
			if (!empty($EF0)) {
				$EF1 = glob("$TMPdir/*/*");
				$EF2 = glob("$TMPdir/*/*/*");
				$EF3 = glob("$TMPdir/*/*/*/*");
				$ExtractedFiles = array_merge($EF0,$EF1,$EF2,$EF3);
				foreach ($ExtractedFiles AS $File) {
					if (is_dir($File)) {
						echo "[dir] $s$s".substr("$File",12)."<br/>\n";
					} else {
						echo "[file] $s$s".substr("$File",12)."<br/>\n";
					}
				}
				
				## ... weitere aktionen mit den Dateien...
				
			} else { echo "<b class='tabred'>Es wurden keine Dateien entpackt!</b>\n"; }
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

?>

</body>
</html>
