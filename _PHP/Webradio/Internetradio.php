<?php
//------------------------------------------------------------------------------
$Playlist = "/var/lib/mpd/playlists/internetradio.m3u";
$MaxRowCounter = 3;
//------------------------------------------------------------------------------
/*
	Edit: /var/lib/mpd/playlists/internetradio.m3u
	and add something like:

http://stream.laut.fm/best_of_80s
http://stream.laut.fm/radiofunclub80
http://stream.laut.fm/maximix
http://stream.laut.fm/eurosmoothjazz
http://stream.laut.fm/jahfari
http://stream.laut.fm/just80s
http://stream.laut.fm/rockin_c

*/

//------------------------------------------------------------------------------
require_once("functions.php");

exec("mpc load ".basename($Playlist, '.m3u'), $output, $return_var);
if (isset($return_var) AND $return_var >= 1) {
	echo "ERROR: <br/>";
	echo exitcode($return_var)."<br/>\n";
}
/*
if (isset($output) AND !empty($output)) {
	echo "output: <br/>";
	foreach($output AS $line) { echo $line."<br/>\n"; }
}
*/
?>
<html>
<head>
<title>Internetradio</title>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>
<script type="text/javascript">
  function control(command){
    $('#result').load("functions.php?cmd="+command);
  }
  function sender(num){
    $('#result').load("functions.php?sender="+num);
  }
  function currentTitle(){
    $('#currentTitle').load("functions.php?cmd=current");
  }
  var intervalID = false;
  function init() {
    if (intervalID) { clearInterval(intervalID); }
    intervalID = setInterval(currentTitle, 1000);
  }
</script>
</head>
<body onload="init();">
<p>
<a href="#" onclick="currentTitle();">Spiele aktuell</a> &#8226;
<a href="#" onclick="control('volume');">Derzeitige Lautstarke</a> &#8226;
<a href="#" onclick="control('leiser');">Leiser</a> &#8226;
<a href="#" onclick="control('lauter');">Lauter</a> &#8226;
<a href="#" onclick="control('stop');">Stop</a>
</p>
<center>
<table border="1" cellpadding="7" cellspacing="1" bordercolorlight>
<?php
$StreamFile = file($Playlist);
$Counter = 0;
foreach($StreamFile AS $line_num => $line) {
	if ($Counter == 0) { echo "<tr>\n"; }
	$Sender = basename($line);
	$SenderCount = $line_num + 1;
	echo "<td><a href='#' onclick='sender(".$SenderCount.");' title=".$SenderCount.">".$Sender."</a></td>\n";
	$Counter++;
	if ($MaxRowCounter == $Counter) { $Counter = 0; echo "</tr>\n"; }
}
echo "</tr>\n";
?>
</table>
</center>
<p><div id="result"></div></p>
<p><div id="currentTitle"></div></p>
</body>
</html>
