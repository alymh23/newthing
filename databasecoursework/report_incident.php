<?php
// 包含数据库连接文件

require_once 'db.inc.php';

// 检查是否通过 POST 方法提交
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 获取表单数据
    $vehicle_id = $_POST['vehicle_id'] ?? null;
    $people_id = $_POST['people_id'] ?? null;
    $incident_date = $_POST['incident_date'] ?? null;
    $incident_report = $_POST['incident_report'] ?? null;
    $offence_id = $_POST['offence_id'] ?? null;

    // 验证输入
    if ($vehicle_id && $people_id && $incident_date && $incident_report && $offence_id) {
        try {
            // 准备并执行 SQL 语句
            $sql = "INSERT INTO Incident (Vehicle_ID, People_ID, Incident_Date, Incident_Report, Offence_ID) 
                    VALUES (?, ?, ?, ?, ?)";
            $stmt = $conn->prepare($sql); // 使用 mysqli 的 prepare 方法
            $stmt->bind_param('iisss', $vehicle_id, $people_id, $incident_date, $incident_report, $offence_id);
            $stmt->execute();
            echo "Incident reported successfully!";
        } catch (mysqli_sql_exception $e) {
            die("Error reporting incident: " . $e->getMessage());
        }
    } else {
        echo "Please fill in all fields.";
    }
}
?>

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Incident</title>
</head>
<body>
    <h1>Report a New Incident</h1>
    <form method="POST" action="">
        <label for="vehicle_id">Vehicle ID:</label>
        <input type="number" id="vehicle_id" name="vehicle_id" required><br>

        <label for="people_id">People ID:</label>
        <input type="number" id="people_id" name="people_id" required><br>

        <label for="incident_date">Incident Date:</label>
        <input type="date" id="incident_date" name="incident_date" required><br>

        <label for="incident_report">Incident Report:</label>
        <textarea id="incident_report" name="incident_report" required></textarea><br>

        <label for="offence_id">Offence ID:</label>
        <input type="number" id="offence_id" name="offence_id" required><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
