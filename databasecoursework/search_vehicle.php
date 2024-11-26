<?php
session_start();
require("db.inc.php");
// 初始化变量
$searchPlate = "";
$searchType = "";
$searchColor = "";
$results = [];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 获取用户输入
    $searchPlate = $conn->real_escape_string($_POST["Vehicle_plate"]);
    $searchType = $conn->real_escape_string($_POST["Vehicle_type"]);
    $searchColor = $conn->real_escape_string($_POST["Vehicle_colour"]);

    // 构建查询语句
    $sql = "SELECT * FROM Vehicle WHERE 1=1";
    if (!empty($searchPlate)) {
        $sql .= " AND Vehicle_plate LIKE '%$searchPlate%'";
    }
    if (!empty($searchType)) {
        $sql .= " AND Vehicle_type LIKE '%$searchType%'";
    }
    if (!empty($searchColor)) {
        $sql .= " AND Vehicle_colour LIKE '%$searchColor%'";
    }

    // 执行查询
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $results[] = $row;
        }
    } else {
        echo "未找到匹配的车辆信息。";
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>车辆信息搜索</title>
</head>
<body>
    <h1>搜索车辆信息</h1>
    <form method="POST" action="search_vehicle.php">
        <label for="vehicle_plate">车牌号:</label>
        <input type="text" id="vehicle_plate" name="vehicle_plate" value="<?php echo htmlspecialchars($searchPlate); ?>"><br><br>

        <label for="vehicle_type">车辆类型:</label>
        <input type="text" id="vehicle_type" name="vehicle_type" value="<?php echo htmlspecialchars($searchType); ?>"><br><br>

        <label for="vehicle_color">车辆颜色:</label>
        <input type="text" id="vehicle_color" name="vehicle_color" value="<?php echo htmlspecialchars($searchColor); ?>"><br><br>

        <input type="submit" value="搜索">
    </form>

    <?php if (!empty($results)): ?>
        <h2>搜索结果:</h2>
        <table border="1">
            <tr>
                <th>车辆ID</th>
                <th>类型</th>
                <th>颜色</th>
                <th>车牌号</th>
            </tr>
            <?php foreach ($results as $vehicle): ?>
                <tr>
                    <td><?php echo htmlspecialchars($vehicle['Vehicle_ID']); ?></td>
                    <td><?php echo htmlspecialchars($vehicle['Vehicle_type']); ?></td>
                    <td><?php echo htmlspecialchars($vehicle['Vehicle_colour']); ?></td>
                    <td><?php echo htmlspecialchars($vehicle['Vehicle_plate']); ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    <?php endif; ?>
</body>
</html>