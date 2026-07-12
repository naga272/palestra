<!DOCTYPE html>
<html>

<body>
<?php

$servername = "172.16.1.99";
$username = "ut19290";
$password = "pw19290";
$dbname = "db19290";


try {
  $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
  $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  //echo "Connected successfully";
} catch(PDOException $e) {
	echo "error" . $e->$getMessage();
}


try {
	$sql = "select * from Libri where autore = \"" . $_POST['autore'] . "\";";
	echo "<br>".$sql;
	$result = $conn->query($sql);
	if ($result->rowCount() > 0) {
		echo "<table>";
		while($tupla = $result->fetch()) {
			echo "<tr>";
			echo "<td>" . $tupla["id_libro"] . "</td>";
			echo "<td>" . $tupla["titolo"] . "</td>";
			echo "<td>" . $tupla["autore"] . "</td>";
			echo "</tr>";
		}
		echo "</table>";
		unset($result);
	} else {
		echo "nessuna riga da mostrare :P";
	}
} catch (PDOException $e) {
	echo "error" . $e->$getMessage();
}

$conn = null;
?>


</body>
</html>