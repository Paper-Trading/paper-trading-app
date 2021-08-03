<?php
$servername = "10.147.20.30";
$username = "jrss";
$password = "dipishpatel";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?> 
