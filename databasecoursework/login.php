<?php
session_start();
require 'db.inc.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // 仅根据用户名查询
    $stmt = $conn->prepare("SELECT * FROM officers WHERE username = ?");
    $stmt->bind_param("s", $username); // 只绑定一个变量
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows === 1) {
        $user = $result->fetch_assoc();

        // 使用 password_verify 验证密码
        if (password_verify($password, $user['password'])) {
            // 密码正确，创建会话
            $_SESSION['username'] = $user['username'];
            $_SESSION['role'] = $user['role'];

            // 根据用户角色重定向
            if ($user['role'] === 'admin') {
                header("Location: admin_manage.php");
            } else {
                header("Location: dashboard.php");
            }
            exit();
        } else {
            echo "密码错误！";
        }
    } else {
        echo "用户名不存在！";
    }
}
?>

<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录</title>
</head>
<body>
    <h1>登录</h1>
    <form method="post" action="">
        <label for="username">用户名:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">密码:</label>
        <input type="password" id="password" name="password" required><br><br>

        <button type="submit">登录</button>
    </form>
</body>
</html>
