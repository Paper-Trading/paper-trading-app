<?php
$hostname = "it490-papertrading.cohssfafs9cm.us-east-2.rds.amazonaws.com";
$username = "jrss";
$password = "dipeshpatel";
$dbname = "it490";
$conn = NULL;

try {
    $conn = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);
    if($conn != null){echo "sucessfully connected";}
} catch(PDOException $e) {
    // echo "Connection failed: " . $e->getMessage();
    http_error("500 Internal Server Error\n\n"."There was a SQL error:\n\n" . $e->getMessage());
}



?>