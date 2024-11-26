<?php
// 开启会话
session_start();

// 检查用户是否登录
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

// 获取用户信息
$username = $_SESSION['username'];
$is_admin = $_SESSION['is_admin'] ?? false;

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .menu {
            margin-top: 20px;
        }
        .menu a {
            display: block;
            margin: 10px 0;
            text-decoration: none;
            color: blue;
        }
    </style>
</head>
<body>
    <h1>Welcome, <?php echo htmlspecialchars($username); ?>!</h1>
    <p>Choose an action below:</p>

    <div class="menu">
        <a href="search_person.php">Search Person Information</a>
        <a href="search_vehicle.php">Search Vehicle Information</a>
        <a href="report_incident.php">Report Traffic Incident</a>
        <a href="add_vehicle.php">Add Vehicle Information</a>

        <?php if ($is_admin): ?>
            <h3>Admin Functions</h3>
            <a href="audit_log.php">View Audit Logs</a>
        <?php endif; ?>
    </div>

    <p><a href="logout.php">Logout</a></p>
</body>
</html>
