<?php
require("db.inc.php");

if ($_SERVER['REQUEST_METHOD'] == 'GET' && !empty($_GET['query'])) {
    $query = $_GET['query'];
    $stmt = $conn->prepare("SELECT * FROM People WHERE People_name LIKE ? OR People_licence = ?");
    $likeQuery = "%$query%";
    $stmt->bind_param("ss", $likeQuery, $query);
    $stmt->execute();
    $result = $stmt->get_result();
    while ($row = $result->fetch_assoc()) {
        echo "name: " . $row['People_name'] . " - licence number: " . $row['People_licence'] . "<br>";
    }
}
?>
<form method="get" action="">
    search: <input type="text" name="query">
    <button type="submit">search</button>
</form>
