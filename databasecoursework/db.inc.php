<?php

// MySQL database information       
$servername = "mariadb";
$username = "root";
$password = "rootpwd";
$dbname = "coursework2";
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

?>