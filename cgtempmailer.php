<?php
/*
	Requires: https://github.com/PHPMailer/PHPMailer/releases/tag/v5.2.6
*/
require_once('PHPMailer_5.2.6/class.phpmailer.php');

$cputemp = file_get_contents("/sys/class/thermal/thermal_zone0/temp") / 1000;
$gputemp = exec("/opt/vc/bin/vcgencmd measure_temp");  
$gputemp = str_replace("temp=","",$gputemp);
$gputemp = str_replace("'C","",$gputemp);

$message="";

if (!empty($cputemp)) { $message.=" CPU Temperature: $cputemp"; }
if (!empty($gputemp) AND !preg_match("/failed/",$gputemp)) { $message.="<br/>\n GPU Temperature: $gputemp"; }


$mail = new PHPMailer(); // create a new object
$mail->IsSMTP(); // enable SMTP
$mail->SMTPDebug = 1; // debugging: 1 = errors and messages, 2 = messages only
$mail->SMTPAuth = true; // authentication enabled
$mail->SMTPSecure = 'ssl'; // secure transfer enabled REQUIRED for GMail
$mail->Host = "smtp.gmail.com";
$mail->Port = 465; // or 587
$mail->IsHTML(true);
$mail->Username = "email@gmail.com";
$mail->Password = 'password';
$mail->SetFrom("example@gmail.com");
$mail->AddAddress("email@gmail.com");

$mail->Subject = "RaspberryPI CPU/GPU Status";
$mail->Body = "$message";

echo $message."<br/>\n";

if (!$mail->Send()) {
	echo "Mailer Error: " . $mail->ErrorInfo;
} else {
	echo "Mail sent!";
}
?>