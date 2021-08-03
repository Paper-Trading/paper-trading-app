<?php
//$hostname = "it490-papertrading.cohssfafs9cm.us-east-2.rds.amazonaws.com";

$hostname = "10.147.20.30:3306";
$username = "jaysen";
$password = "passwordit490";
$dbname = "it490";
$conn = NULL;

try {
    $conn = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);
    
    $createQuery = "CREATE TABLE testTable (Username VARCHAR(16), Password VARCHAR(16))";
    $conn->exec($createQuery);
    
    
    if($conn != null){echo "sucessfully connected";}
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}

?>
