<?php
session_start();
require("db.inc.php");

if (!isset($_SESSION["user"]) || $_SESSION["role"] !== "admin") {
    header("Location: index.php");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];
    $email = $_POST["email"];
    $role = $_POST["role"];

    try {
        $stmt = $conn->prepare("INSERT INTO Users (Username, Password, Email, Role) VALUES (:username, :password, :email, :role)");
        $stmt->execute(["username" => $username, "password" => $password, "email" => $email, "role" => $role]);
        echo "User added successfully!";
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Add User</title>
</head>
<body>
    <h1>Add New User</h1>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required>
        <br>
        <label>Password:</label>
        <input type="password" name="password" required>
        <br>
        <label>Email:</label>
        <input type="email" name="email" required>
        <br>
        <label>Role:</label>
        <select name="role" required>
            <option value="user">User</option>
            <option value="admin">Admin</option>
        </select>
        <br>
        <button type="submit">Add User</button>
    </form>
</body>
</html>
