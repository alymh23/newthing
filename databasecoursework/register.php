<?php
require('db.inc.php');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'];
    $username = $_POST['username'];
    $password = $_POST['password'];
    $role = $_POST['role'];

    // 检查用户名是否已存在
    $stmt = $conn->prepare("SELECT * FROM officers WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        // 将错误信息保存到变量中
        $error = "用户名已存在，请选择其他用户名。";
    } else {
        // 插入新用户
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT);
        $stmt = $conn->prepare("INSERT INTO officers (name, username, password, role) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("ssss", $name, $username, $hashedPassword, $role);

        if ($stmt->execute()) {
            // 成功注册，重定向到登录页面
            header("Location: login.php");
            exit();
        } else {
            // 将错误信息保存到变量中
            $error = "注册失败，请稍后重试。";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>注册</title>
</head>
<body>
    <h1>注册账户</h1>

    <!-- 显示错误信息 -->
    <?php if (!empty($error)): ?>
        <p style="color: red;"><?php echo htmlspecialchars($error); ?></p>
    <?php endif; ?>

    <form method="post" action="register.php">
        <label for="name">name:</label>
        <input type="text" id="name" name="name" required><br><br>

        <label for="username">user name:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <label for="role">role:</label>
        <select id="role" name="role" required>
            <option value="officer">officer</option>
            <option value="admin">admin</option>
        </select><br><br>

        <button type="submit">register</button>
    </form>
    <p>already have account？<a href="login.php">login</a></p>
</body>
</html>
