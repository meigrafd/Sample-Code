<?php

$AGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1";
ini_set('user_agent', $AGENT);

$regex = "<h2 class=\"entry-title\"><a href=\"(.*)\" rel=\"bookmark\" title=\".*\">(.*)<\/a><\/h2>";
$input = @file_get_contents("http://www.mydealz.de/") OR die("Could not access: http://www.mydealz.de/");

if (preg_match_all("/$regex/siU", $input, $matches)) {
	foreach ($matches[2] AS $c => $match) {
		$DEALtext = htmlspecialchars_decode("$match",ENT_QUOTES);
		$DEALurl = $matches[1][$c];
		echo "$c\n";
		echo "$DEALtext\n";
		echo "$DEALurl\n";
		#http://www.mydealz.de/27880/transcend-jetflash-780-fur-30e-sehr-schneller-usb-3-0-stick/
		$regexID = "http\:\/\/www.mydealz.de\/(.*)\/.*";
		if (preg_match_all("/$regexID/siU", $DEALurl, $matchesID)) {
			$DEALid = $matchesID[1][0];
		}
		
		#print_r($matches[1][$c]);
		echo "\n-----\n";
	}
	#print_r($matches);
}

?>