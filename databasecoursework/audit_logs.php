<?php
// 包含数据库连接信息
require_once 'db.inc.php';
session_start();

// 检查用户是否登录且为管理员
if (!isset($_SESSION['user']) || $_SESSION['user']['role'] !== 'admin') {
    header("Location: login.php");
    exit("Access denied.");
}

try {
    // 获取审计日志
    $sql = "SELECT a.id, a.user_id, o.name AS username, a.action, a.record_id, a.timestamp, a.details
            FROM audit_log a
            JOIN officers o ON a.user_id = o.id
            ORDER BY a.timestamp DESC";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    $log = $stmt->fetch(PDO::FETCH_ASSOC); // 确保返回的是数组
} catch (PDOException $e) {
    die("Error retrieving logs: " . $e->getMessage());
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audit Logs</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Audit Logs</h1>
    <?php if (!empty($log)): ?>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Action</th>
                    <th>Record ID</th>
                    <th>Timestamp</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($logs as $log): ?>
                    <tr>
                        <td><?= htmlspecialchars($log['id']) ?></td>
                        <td><?= htmlspecialchars($log['username']) ?></td>
                        <td><?= htmlspecialchars($log['action']) ?></td>
                        <td><?= htmlspecialchars($log['record_id'] ?? 'N/A') ?></td>
                        <td><?= htmlspecialchars($log['timestamp']) ?></td>
                        <td><?= htmlspecialchars($log['details'] ?? 'N/A') ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php else: ?>
        <p>No logs found.</p>
    <?php endif; ?>
</body>
</html>
