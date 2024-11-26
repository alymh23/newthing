<?php 
// 包含数据库连接配置
require_once 'db.inc.php';

// 初始化错误信息
$error = '';
$success = '';

// 处理表单提交
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $reg_plate = $_POST['reg_plate'];
    $make = $_POST['make'];
    $model = $_POST['model'];
    $color = $_POST['color'];
    $owner_license = $_POST['owner_license'];
    $owner_name = $_POST['owner_name'];
    $owner_address = $_POST['owner_address'];

    // 验证用户输入
    if (empty($reg_plate) || empty($make) || empty($model) || empty($color) || empty($owner_license)) {
        $error = "请填写所有必填字段！";
    } else {
        try {
            // 检查数据库中是否已存在车辆
            $stmt = $pdo->prepare("SELECT * FROM Ownership WHERE Vehicle_ID = (SELECT Vehicle_ID FROM Vehicles WHERE Vehicle_reg = ?)");
            $stmt->execute([$reg_plate]);

            if ($stmt->rowCount() > 0) {
                $error = "该车牌号已存在！";
            } else {
                // 检查车主是否已存在
                $stmt = $pdo->prepare("SELECT * FROM People WHERE People_licence = ?");
                $stmt->execute([$owner_license]);
                
                if ($stmt->rowCount() == 0) {
                    // 添加新车主
                    $stmt = $pdo->prepare("INSERT INTO People (People_name, People_address, People_licence) VALUES (?, ?, ?)");
                    $stmt->execute([$owner_name, $owner_address, $owner_license]);
                }

                // 添加车辆信息
                $stmt = $pdo->prepare("INSERT INTO Vehicles (Vehicle_reg, Vehicle_make, Vehicle_model, Vehicle_colour) VALUES (?, ?, ?, ?)");
                $stmt->execute([$reg_plate, $make, $model, $color]);

                // 获取新插入的车辆 ID
                $vehicle_id = $pdo->lastInsertId();

                // 添加到 Ownership 表
                $stmt = $pdo->prepare("INSERT INTO Ownership (People_ID, Vehicle_ID) VALUES (
                    (SELECT People_ID FROM People WHERE People_licence = ?), 
                    ?
                )");
                $stmt->execute([$owner_license, $vehicle_id]);

                $success = "车辆已成功添加！";
            }
        } catch (Exception $e) {
            $error = "数据库操作失败：" . $e->getMessage();
        }
    }
}
?>

<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>添加车辆</title>
</head>
<body>
    <h1>添加车辆信息</h1>

    <?php if (!empty($error)): ?>
        <p style="color: red;"><?php echo $error; ?></p>
    <?php endif; ?>

    <?php if (!empty($success)): ?>
        <p style="color: green;"><?php echo $success; ?></p>
    <?php endif; ?>

    <form method="post" action="add_vehicle.php">
        <label for="reg_plate">车牌号：</label>
        <input type="text" id="reg_plate" name="reg_plate" required><br>

        <label for="make">品牌：</label>
        <input type="text" id="make" name="make" required><br>

        <label for="model">型号：</label>
        <input type="text" id="model" name="model" required><br>

        <label for="color">颜色：</label>
        <input type="text" id="color" name="color" required><br>

        <label for="owner_license">车主驾照号：</label>
        <input type="text" id="owner_license" name="owner_license" required><br>

        <label for="owner_name">车主姓名：</label>
        <input type="text" id="owner_name" name="owner_name"><br>

        <label for="owner_address">车主地址：</label>
        <input type="text" id="owner_address" name="owner_address"><br>

        <button type="submit">添加车辆</button>
    </form>
</body>
</html>
