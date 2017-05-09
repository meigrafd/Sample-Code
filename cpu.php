<?php
/*

 v0.9 - Written by meigrafd
 
 http://www.forum-raspberrypi.de/Thread-php-cpu-sys-infos

 /opt/vc/bin/vcgencmd support to get detailed Infos. Warning: makes much more CPU load!

 required /etc/sudoers entry to display GPU Temp , CPU Voltage and all other vcgencmd-values:

 www-data ALL=NOPASSWD:/opt/vc/bin/vcgencmd

*/
session_start();
session_cache_expire(1440);
$DURATION_start = microtime(true);
$ERROR = "";
$CMD = 'sudo /opt/vc/bin/vcgencmd';
$USEvcgencmd = 0;	// set 1 to default enable it
$DISPLAYfreespace = 1;	// set 0 to disable
$PageRefresh = "10";	// Refresh Page every ... Sec
define("TEMP_PATH","/tmp/");

# get RaspberryPI Revision
if (!file_exists("/tmp/.rpi_rev")) {
	GetRPIrev();
	WriteRPIrev($RPIrev,$RPIrevinfo);
	$RPIrevision = "RaspberryPI Revision: $RPIrev ($RPIrevinfo)";
} else {
	$RPIrevision = file_get_contents("/tmp/.rpi_rev");
}

$RESET = isset($_POST["RESET"]) ? $_POST["RESET"] : "";
$buttonUSEvcgencmd = isset($_POST["USEvcgencmd"]) ? $_POST["USEvcgencmd"] : "";

if (!empty($buttonUSEvcgencmd)) {
	if ($buttonUSEvcgencmd == "true") { $_SESSION['vcgencmd'] = 1; }
	if ($buttonUSEvcgencmd == "false") { $_SESSION['vcgencmd'] = 0; }
}

if (isset($_SESSION['vcgencmd']) AND $_SESSION['vcgencmd'] == 1) {
	$USEvcgencmd = 1;
} elseif (isset($_SESSION['vcgencmd']) AND $_SESSION['vcgencmd'] == 0) {
	$USEvcgencmd = 0;
}

if (!isset($vcgencmd)) { $vcgencmd=0; }

if (!empty($RESET)) {
	if (isset($_SESSION['max_cputemp'])) { unset($_SESSION['max_cputemp']); }
	if (isset($_SESSION['min_cputemp'])) { unset($_SESSION['min_cputemp']); }
	if (isset($_SESSION['max_cpufreq'])) { unset($_SESSION['max_cpufreq']); }
	if (isset($_SESSION['min_cpufreq'])) { unset($_SESSION['min_cpufreq']); }
	if (isset($_SESSION['max_gputemp'])) { unset($_SESSION['max_gputemp']); }
	if (isset($_SESSION['min_gputemp'])) { unset($_SESSION['min_gputemp']); }
}

$cputemp = trim(file_get_contents("/sys/class/thermal/thermal_zone0/temp")) / 1000;
$cpufreq = trim(file_get_contents("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")) / 1000;

# vcgencmd command details: http://elinux.org/RPI_vcgencmd_usage
if (isset($USEvcgencmd) AND $USEvcgencmd == 1) {
	if (!file_exists("/opt/vc/bin/vcgencmd")) {
		$ERROR = "Error while executing '".$CMD."'!<br/>Cant find /opt/vc/bin/vcgencmd Shellcommand!";
		$USEvcgencmd = 0;
	} else {
		@exec("".$CMD." measure_temp", $gputemp);
		if (!empty($gputemp[0])) {
			if (preg_match("/VCHI initialization failed/", $gputemp[0])) {
				$ERROR = "Error while executing '".$CMD."'! $gputemp[0]<br/>Maybe no sudo prefix or you forgot the required entry in /etc/sudoers ?";
			} else {
				$vcgencmd = 1;
				preg_match("/.*=(.*)/", $gputemp[0], $gmatch);
				if (isset($gmatch[1])) { $gputemp[0] = str_replace("'C", "", $gmatch[1]); } else { unset($gputemp[0]); }
				unset($gmatch);
			}
		} else {
			$ERROR = "Error while executing '".$CMD."'!<br/>Maybe no sudo prefix or you forgot the required entry in /etc/sudoers ?";
		}
		if (isset($vcgencmd) AND $vcgencmd == 1) {
			# current active volts
			$VoltTypes = "core sdram_c sdram_i sdram_p";
			$volt_list = array();
			foreach (explode(" ", $VoltTypes) AS $vt) {
				preg_match("/.*=(.*)/", exec("".$CMD." measure_volts ".$vt.""), $vmatch);
				if (isset($vmatch[1])) { $volt_list["$vt"] = $vmatch[1]; }
				unset($vmatch);
			}
			# current active settings
			exec("".$CMD." get_config int", $config_integers);
			$config_integer = array();
			foreach ($config_integers AS $integer) {
				preg_match('°(.*)=(.*)°', $integer,$int);
				if (isset($int[1]) AND !empty($int[1])) { $config_integer["$int[1]"] = $int[2]; }
				unset($int);
			}
			# current active frequency's
			$ClockTypes = "arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi";
			$clock_list = array();
			foreach (explode(" ", $ClockTypes) AS $ct) {
				preg_match("/.*=(.*)/", exec("".$CMD." measure_clock ".$ct.""), $clmatch);
				if (isset($clmatch[1])) { $clock_list["$ct"] = $clmatch[1]; }
				unset($clmatch);
			}
			# current codec enabled
			$CodecTypes = "H264 MPG2 WVC1 MPG4 MJPG WMV9";
			$codec_list = array();
			foreach (explode(" ", $CodecTypes) AS $ct) {
				preg_match("/.*=(.*)/", exec("".$CMD." codec_enabled ".$ct.""), $cmatch);
				if (isset($cmatch[1])) { $codec_list["$ct"] = $cmatch[1]; }
				unset($cmatch);
			}
			# current mem split
			$MemTypes = "arm gpu";
			$mem_list = array();
			foreach (explode(" ", $MemTypes) AS $mt) {
				preg_match("/.*=(.*)/", exec("".$CMD." get_mem ".$mt.""), $mmatch);
				if (isset($mmatch[1])) { $mem_list["$mt"] = $mmatch[1]; }
				unset($mmatch);
			}
		}
	}
}

# Display Free Space
if (isset($DISPLAYfreespace) AND $DISPLAYfreespace == 1) {
	$FreeSpace ="<table id='FreeSpace' cellspacing='0' border='1px'>\n";
	$FreeSpace.="<tr><th colspan='6'>Free Space on: ".$_SERVER['SERVER_NAME']."</th></tr>\n";
	$FreeSpace.="<tr style='font-weight:bold; text-align:center;'>\n";
	$FreeSpace.="<td> Filesystem </td><td> Size </td><td> Used </td><td> Free </td><td> % Used </td><td> Mountpoint </td>\n";
	$FreeSpace.="</tr>\n";
	exec("df -h", $DiskFree);
	array_shift($DiskFree);
	foreach ($DiskFree AS $DFline) {
		$c=0;
		$FreeSpace.="<tr>\n";
		foreach(explode(" ",$DFline) AS $DFrow) {
			if (empty($DFrow) AND $DFrow !== "0") { continue; }
			++$c;
			if ($c > "1" AND $c != "6" AND $pos = strpos($DFrow,".0")) {
				$prefix = substr($DFrow,-1);
				$DFrow = "".substr($DFrow,0,$pos)."".$prefix."";
			}
			if ($c > "1" AND $c < "5") {
				$DFrow = str_replace("B"," B",$DFrow);
				$DFrow = str_replace("K"," KB",$DFrow);
				$DFrow = str_replace("M"," MB",$DFrow);
				$DFrow = str_replace("G"," GB",$DFrow);
			}
			if ($c >= "2" AND $c != "6") { $td="<td style='text-align:right;'>"; } else { $td="<td>"; }
			$FreeSpace.="".$td." ".$DFrow." </td>";
		}
		$FreeSpace.="\n</tr>\n";
	}
	$FreeSpace.="</table>\n";
}


// max cpu
if (!isset($_SESSION['max_cputemp'])) {
	$_SESSION['max_cputemp'] = $cputemp;
} elseif ($_SESSION['max_cputemp'] < $cputemp) {
	$_SESSION['max_cputemp'] = $cputemp;
}
if (!isset($_SESSION['max_cpufreq'])) {
	$_SESSION['max_cpufreq'] = $cpufreq;
} elseif ($_SESSION['max_cpufreq'] < $cpufreq) {
	$_SESSION['max_cpufreq'] = $cpufreq;
}
// min cpu
if (!isset($_SESSION['min_cputemp'])) {
	$_SESSION['min_cputemp'] = $cputemp;
} elseif ($cputemp < $_SESSION['min_cputemp']) {
	$_SESSION['min_cputemp'] = $cputemp;
}
if (!isset($_SESSION['min_cpufreq'])) {
	$_SESSION['min_cpufreq'] = $cpufreq;
} elseif ($cpufreq < $_SESSION['min_cpufreq']) {
	$_SESSION['min_cpufreq'] = $cpufreq;
}

if (isset($vcgencmd) AND $vcgencmd == 1 AND isset($gputemp[0])) {
	// max gpu
	if (!isset($_SESSION['max_gputemp'])) {
		$_SESSION['max_gputemp'] = $gputemp[0];
	} elseif ($_SESSION['max_gputemp'] < $gputemp[0]) {
		$_SESSION['max_gputemp'] = $gputemp[0];
	}
	// min gpu
	if (!isset($_SESSION['min_gputemp'])) {
		$_SESSION['min_gputemp'] = $gputemp[0];
	} elseif ($gputemp[0] < $_SESSION['min_gputemp']) {
		$_SESSION['min_gputemp'] = $gputemp[0];
	}
}

class CPULoad {
	function check_load() {
		$fd = fopen("/proc/stat","r");
		if ($fd) {
			$statinfo = explode("\n",fgets($fd, 1024));
			fclose($fd);
			foreach($statinfo as $line) {
				$info = explode(" ",$line);
				//echo "<pre>"; var_dump($info); echo "</pre>";
				if($info[0]=="cpu") {
					array_shift($info);  // pop off "cpu"
					if(!$info[0]) array_shift($info); // pop off blank space (if any)
					$this->user = $info[0];
					$this->nice = $info[1];
					$this->system = $info[2];
					$this->idle = $info[3];
//					$this->print_current();
					return;
				}
			}
		}
	}
	function store_load() {
		$this->last_user = $this->user;
		$this->last_nice = $this->nice;
		$this->last_system = $this->system;
		$this->last_idle = $this->idle;
	}
	function save_load() {
		$this->store_load();
		$fp = @fopen(TEMP_PATH."cpuinfo.tmp","w");
		if ($fp) {
			fwrite($fp,time()."\n");
			fwrite($fp,$this->last_user." ".$this->last_nice." ".$this->last_system." ".$this->last_idle."\n");
			fwrite($fp,$this->load["user"]." ".$this->load["nice"]." ".$this->load["system"]." ".$this->load["idle"]." ".$this->load["cpu"]."\n");
			fclose($fp);
		}
	}
	function load_load() {
		$fp = @fopen(TEMP_PATH."cpuinfo.tmp","r");
		if ($fp) {
			$lines = explode("\n",fread($fp,1024));
			$this->lasttime = $lines[0];
			list($this->last_user,$this->last_nice,$this->last_system,$this->last_idle) = explode(" ",$lines[1]);
			list($this->load["user"],$this->load["nice"],$this->load["system"],$this->load["idle"],$this->load["cpu"]) = explode(" ",$lines[2]);
			fclose($fp);
		} else {
			$this->lasttime = time() - 60;
			$this->last_user = $this->last_nice = $this->last_system = $this->last_idle = 0;
			$this->user = $this->nice = $this->system = $this->idle = 0;
		}
	}
	function calculate_load() {
		//$this->print_current();
		$d_user = $this->user - $this->last_user;
		$d_nice = $this->nice - $this->last_nice;
		$d_system = $this->system - $this->last_system;
		$d_idle = $this->idle - $this->last_idle;
		//printf("Delta - User: %f  Nice: %f  System: %f  Idle: %f<br/>",$d_user,$d_nice,$d_system,$d_idle);
		$total=$d_user+$d_nice+$d_system+$d_idle;
		if ($total<1) $total=1;
		$scale = 100.0/$total;
		$cpu_load = ($d_user+$d_nice+$d_system)*$scale;
		$this->load["user"] = $d_user*$scale;
		$this->load["nice"] = $d_nice*$scale;
		$this->load["system"] = $d_system*$scale;
		$this->load["idle"] = $d_idle*$scale;
		$this->load["cpu"] = ($d_user+$d_nice+$d_system)*$scale;
	}
	function print_current() {
		printf("Current load tickers - User: %f  Nice: %f  System: %f  Idle: %f<br/>",
			$this->user,
			$this->nice,
			$this->system,
			$this->idle
		);
	}
	function print_load() {
		printf("User: %.1f%%  Nice: %.1f%%  System: %.1f%%  Idle: %.1f%%  Load: %.1f%%<br/>",
			$this->load["user"],
			$this->load["nice"],
			$this->load["system"],
			$this->load["idle"],
			$this->load["cpu"]
		);
	}
	function get_load($fastest_sample=4) {
		$this->load_load();
		$this->cached = (time()-$this->lasttime);
		if ($this->cached>=$fastest_sample) {
			$this->check_load(); 
			$this->calculate_load();
			$this->save_load();
		}
	}
}

function print_LoadColor($x) {
	if ($x  >= 90) { return "#FF0000"; }
	elseif (($x  >= 70) && ($x  <= 89)) { return "#FF4000"; }
	elseif (($x  >= 60) && ($x  <= 69)) { return "#FF8000"; }
	elseif (($x  >= 50) && ($x  <= 59)) { return "#FFBF00"; }
	elseif (($x  >= 30) && ($x  <= 49)) { return "#FFFF00"; }
	elseif (($x  >= 20) && ($x  <= 29)) { return "#BFFF00"; }
	elseif (($x  >= 10) && ($x  <= 19)) { return "#80FF00"; }
	else  { return "#00FF00"; }
}
# Debug
function showarray($array) {
	echo "<pre>\n";
	var_dump($array);
	echo "\n</pre>\n";
	flush();
}

function GetRPIrev() {
	global $RPIrev,$RPIrevinfo,$overvolted;
	$CPUrev["Beta"] = "1";
	$REVinfos["Beta"] = "Released: Q1 2012, MODEL: B, PCB Version: ?, MEM: 256";
	$CPUrev["0002"] = "1";
	$REVinfos["0002"] = "Released: Q1 2012, MODEL: B, PCB Version: 1.0, MEM: 256";
	$CPUrev["0003"] = "1";
	$REVinfos["0003"] = "Released: Q3 2012, MODEL: B, PCB Version: 1.0, MEM: 256";

	$CPUrev["0004"] = "2";
	$REVinfos["0004"] = "Released: Q3 2012, MODEL: B, PCB Version: 2.0, MEM: 256 (Sony)";
	$CPUrev["0005"] = "2";
	$REVinfos["0005"] = "Released: Q4 2012, MODEL: B, PCB Version: 2.0, MEM: 256 (Qisda)";
	$CPUrev["0006"] = "2";
	$REVinfos["0006"] = "Released: Q4 2012, MODEL: B, PCB Version: 2.0, MEM: 256 (Egoman)";
	$CPUrev["0007"] = "2";
	$REVinfos["0007"] = "Released: Q1 2013, MODEL: A, PCB Version: 2.0, MEM: 256 (Egoman)";
	$CPUrev["0008"] = "2";
	$REVinfos["0008"] = "Released: Q1 2013, MODEL: A, PCB Version: 2.0, MEM: 256 (Sony)";
	$CPUrev["0009"] = "2";
	$REVinfos["0009"] = "Released: Q1 2013, MODEL: A, PCB Version: 2.0, MEM: 256 (Qisda)";
	$CPUrev["000d"] = "2";
	$REVinfos["000d"] = "Released: Q4 2012, MODEL: B, PCB Version: 2.0, MEM: 512 (Egoman)";
	$CPUrev["000e"] = "2";
	$REVinfos["000e"] = "Released: Q4 2012, MODEL: B, PCB Version: 2.0, MEM: 512 (Sony)";
	$CPUrev["000f"] = "2";
	$REVinfos["000f"] = "Released: Q4 2012, MODEL: B, PCB Version: 2.0, MEM: 512 (Qisda)";

	$CPUrev["0010"] = "2";
	$HARDWARErev["0010"] = "BCM2708";
	$REVinfos["0010"] = "Released: Q3 2014, MODEL: B+, PCB Version: 1.2, MEM: 512 (Sony)";
	$CPUrev["0011"] = "2";
	$HARDWARErev["0011"] = "BCM2708";
	$REVinfos["0011"] = "Released: Q2 2014, MODEL: Compute Module, PCB Version: 1.0, MEM: 512 (Sony)";
	$CPUrev["0012"] = "2";
	$HARDWARErev["0012"] = "BCM2708";
	$REVinfos["0012"] = "Released: Q4 2014, MODEL: A+, PCB Version: 1.1, MEM: 256 (Sony)";

	$CPUrev["a01041"] = "3";
	$HARDWARErev["a01041"] = "BCM2709";
	$REVinfos["a01041"] = "Released: Q1 2015, MODEL: Pi2B, PCB Version: 1.1, MEM: 1024 (Sony, UK)";
	$CPUrev["a21041"] = "3";
	$HARDWARErev["a21041"] = "BCM2709";
	$REVinfos["a21041"] = "Released: Q1 2015, MODEL: Pi2B, PCB Version: 1.1, MEM: 1024 (Embest, China)";

	$CPUrev["900092"] = "3";
	$HARDWARErev["900092"] = "BCM2708";
	$REVinfos["900092"] = "Released: Q4 2015, MODEL: PiZero, PCB Version: 1.2, MEM: 512 (Sony, UK)";
    
	$CPUrev["a02082"] = "4";
	$HARDWARErev["a02082"] = "BCM2709";
	$REVinfos["a02082"] = "Released: Q3 2015, MODEL: Pi3B, PCB Version: 1.2, MEM: 1024 (Sony, UK)";
	$CPUrev["a22082"] = "4";
	$HARDWARErev["a22082"] = "BCM2709";
	$REVinfos["a22082"] = "Released: Q1 2016, MODEL: Pi3B, PCB Version: 1.2, MEM: 1024 (Embest, China)";
    
	$cpuinfolines = file("/proc/cpuinfo");
	$FOUND="";
	foreach($cpuinfolines AS $line) {
		if (preg_match("/^Revision.*:(.*)/", $line, $find)) {
			foreach($CPUrev AS $rev => $revision) {
				if (preg_match("/$rev/", $find[1])) {
					$FOUND = $rev;
					if (strlen($find[1]) != 4) { $overvolted = "This Pi has/is overvolted!"; }
				}
			}
		}
	}
	if (!empty($FOUND)) {
		$RPIrev = $CPUrev[$FOUND];
		$RPIrevinfo = $REVinfos[$FOUND];
	}
}

function WriteRPIrev($RPIrev,$RPIinfo) {
	if ($fh = fopen("/tmp/.rpi_rev", "w")) {
		fwrite($fh, "RaspberryPI Revision: $RPIrev ($RPIinfo)");
		fclose($fh);
	}
}
?>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
<title><?php echo $_SERVER['SERVER_NAME']; ?> - Informations</title>
<meta HTTP-EQUIV=Refresh CONTENT='<?php echo $PageRefresh; ?>'>
<style type=text/css>

div { border:1px solid #ccf; }

 body {
	font-size: 8pt;
	color: black;
	font-family: Verdana,arial,helvetica,serif;
	margin: 0 0 0 0;
 }
 .style1 {
	color: #999999;
	font-weight: bold;
 }
 div.progressbar {
	border: 1px solid gray;
	border-style: dotted;
	width: 40%;
	padding: 1px;
	background-color: #E0E0E0;
	margin: 0px;
 }
 div.progressbar div {
	height: 11px;
	background-color: #ff0000;
	width: 0%;
 }
 #vcgencmd {
	position:absolute;
	top:0px;
	left:700px;
	letter-spacing:0px;
	font-family:verdana, arial, helvetica, verdana, tahoma, sans-serif;
 }
 h2 {
	letter-spacing:2px;
	font-family: "Trebuchet MS",verdana,arial, helvetica, verdana, tahoma, sans-serif;
	font-size:24px;
	font-weight:bold;
	text-align:left;
 }
</style>
</head>
<body>
<?php
if (isset($ERROR) AND !empty($ERROR)) {
	$e="font-size:20px; text-align:left; color:firebrick; font-weight:bold;";
	echo "<b style='".$e."'>".$ERROR."</b><br/><br/>\n";
}
?>
<blockquote>
<pre>
<table border="0" cellpadding="0" cellspacing="0">
 <tr>
  <td align="left" valign="top">
   <form name='reset' action='' method='POST'>
    <button type='submit' value='true' name='RESET'>Reset</button>
   </form>
  </td>
<?php
if (file_exists("/opt/vc/bin/vcgencmd")) {
?>
  <td align="right" valign="top">
   <form name='vcgencmd' action='' method='POST'>
    <button type='submit' value='true' name='USEvcgencmd' class='USEvcgencmd'>Use vcgencmd</button>
   </form>
  </td>
  <td align="left" valign="top">
   <form name='vcgencmd' action='' method='POST'>
    <button type='submit' value='false' name='USEvcgencmd' class='USEvcgencmd'>Dont use vcgencmd</button>
   </form>
  </td>
<?php
}
?>
 </tr>
</table>

<?php echo $RPIrevision; ?>

<table border="0" cellpadding="2" cellspacing="0">
 <tr>
  <td>
   <table border="1" cellpadding="5" cellspacing="0">
    <tr align="center" valign="middle"><td colspan="3"><b>CPU Temperature</b></td></tr>
    <tr align="center" valign="middle"><td>Current</td> <td>Max</td> <td>Min</td></tr>
    <tr>
     <td><?php echo $cputemp; ?> &deg;C</td>
     <td><?php echo $_SESSION['max_cputemp']; ?> &deg;C</td>
     <td><?php echo $_SESSION['min_cputemp']; ?> &deg;C</td>
    </tr>
   </table>
  </td>
  <td>
   <table border="1" cellpadding="5" cellspacing="0">
    <tr align="center" valign="middle"><td colspan="3"><b>CPU Frequence</b></td></tr>
    <tr align="center" valign="middle"><td>Current</td> <td>Max</td> <td>Min</td></tr>
    <tr>
     <td><?php echo $cpufreq; ?> MHz</td>
     <td><?php echo $_SESSION['max_cpufreq']; ?> MHz</td>
     <td><?php echo $_SESSION['min_cpufreq']; ?> MHz</td>
    </tr>
   </table>
  </td>
<?php
if (isset($vcgencmd) AND $vcgencmd == 1 AND isset($gputemp[0])) {
?>
  <td>
   <table border="1" cellpadding="5" cellspacing="0">
    <tr align="center" valign="middle"><td colspan="3"><b>GPU Temperature</b></td></tr>
    <tr align="center" valign="middle"><td>Current</td> <td>Max</td> <td>Min</td></tr>
    <tr>
     <td><?php echo $gputemp[0]; ?> &deg;C</td>
     <td><?php echo $_SESSION['max_gputemp']; ?> &deg;C</td>
     <td><?php echo $_SESSION['min_gputemp']; ?> &deg;C</td>
    </tr>
   </table>
  </td>
 </tr>
<?php
}
?>
</table>

<?php
if (isset($DISPLAYfreespace) AND $DISPLAYfreespace == 1) { echo $FreeSpace; }

if (isset($vcgencmd) AND $vcgencmd == 1) {
	// arrays: $config_integer $volt_list $clock_list $codec_list $mem_list
	echo "<div id='vcgencmd'>\n";
	echo " <table border='0' cellpadding='2' cellspacing='0'>\n";
	echo "  <tr>\n";
	echo "   <td>\n";
	echo "    <table border='1' cellspacing='0'>\n";
	echo "     <tr align='center' valign='middle'><td colspan='2'><b>config.txt integers:</b></td></tr>\n";
	foreach ($config_integer AS $type => $int) {
		echo "     <tr><td> ".$type." </td> <td> ".$int." </td></tr>\n";
	}
	echo "    </table>\n";
	echo "   </td>\n";
	echo "   <td>\n";
	echo "    <table border='1' cellspacing='0'>\n";
	echo "     <tr align='center' valign='middle'><td colspan='2'><b>Frequences:</b></td></tr>\n";
	foreach ($clock_list AS $type => $int) {
		echo "     <tr><td> ".$type." </td> <td> ".$int." </td></tr>\n";
	}
	echo "    </table>\n";
	echo "   </td>\n";
	echo "  </tr>\n";
	echo "  <tr>\n";
	echo "   <td>\n";
	echo "    <table border='1' cellspacing='0'>\n";
	echo "     <tr align='center' valign='middle'><td colspan='2'><b>Codecs:</b></td></tr>\n";
	foreach ($codec_list AS $type => $int) {
		echo "     <tr><td> ".$type." </td> <td> ".$int." </td></tr>\n";
	}
	echo "    </table>\n";
	echo "   </td>\n";
	echo "   <td>\n";
	echo "    <table border='1' cellspacing='0'>\n";
	echo "     <tr align='center' valign='middle'><td colspan='2'><b>Volts:</b></td></tr>\n";
	foreach ($volt_list AS $type => $int) {
		echo "     <tr><td> ".$type." </td> <td> ".$int." </td></tr>\n";
	}
	echo "    </table>\n";
	echo "   </td>\n";
	echo "  </tr>\n";
	echo "  <tr>\n";
	echo "   <td>\n";
	echo "    <table border='1' cellspacing='0'>\n";
	echo "     <tr align='center' valign='middle'><td colspan='2'> <b>Mem-Split:</b> </td></tr>\n";
	foreach ($mem_list AS $type => $int) {
		echo "    <tr><td> ".$type." </td> <td> ".$int." </td></tr>\n";
	}
	echo "    </table>\n";
	echo "   </td>\n";
	echo "  </tr>\n";
	echo " </table>\n";
	echo "</div>\n";
}
?>

<span class="style1">Kernel Information:</span>
<?php echo php_uname(); ?><br/>

<span class="style1">Uptime:</span> 
<?php system("uptime"); ?>

<span class="style1">Memory Usage (MB):</span> 
<?php system("free -m"); ?>

</pre>
<p>
<?php
echo "<span class='style1'>CPU Load:</span><br/>\n";
$cpuload = new CPULoad();
$cpuload->get_load();
$cpuload->print_load();
$CPULOAD = round($cpuload->load["cpu"],3);
echo "<br/>The average CPU load is: ".$CPULOAD."%\n";
echo "<div class='progressbar'>\n";
echo " <div style='width: ".$CPULOAD."%; background-color: ".print_LoadColor($CPULOAD).";' id='serviceload'>\n";
echo " </div>\n";
echo "</div>\n";

echo "<br/><br/><br/>";
$DURATION_end = microtime(true);
$DURATION = $DURATION_end - $DURATION_start;
echo "<p><font size='0'>Page generated in ".round($DURATION, 3)." seconds</font></p>\n";
?>
</p>
</blockquote>

</body>
</html>