<?php
// 启动会话
session_start();

// 检查用户是否已登录
if (isset($_SESSION['username'])) {
    echo "<h1>Welcome back，" . htmlspecialchars($_SESSION['username']) . "!</h1>";
    echo "<a href='logout.php'>logout</a>";
} else {
    echo "<h1>Welcome to the Traffic Police Database System</h1>";
    echo "<a href='login.php'>login</a> | <a href='register.php'>register</a>";
}
?>
