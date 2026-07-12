<a href="index.php">torna alla homepage</a>

<?php

$debug = 1;

if ($debug) {
    ini_set("display_errors", 1);
    error_reporting(E_ALL);    
}


function get_conn_db($host, $dbname, $hostname, $password)
{
    try {
        $conn = new PDO(
            "mysql:host={$host};dbname={$dbname};port=3306",
            $hostname,
            $password,
            array(PDO::ATTR_PERSISTENT)
        );
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $conn;
 
    } catch (PDOException $err) {
        echo $err->getMessage();
        exit;
    }

}


function do_query($conn) {
    $sql_q = "select * from Prodotti";
    $sttm = $conn->prepare($sql_q);
    $sttm->execute();
    
    $response = $sttm->fetchAll(PDO::FETCH_ASSOC);
    return $response;
}


function display_table($entries_table, $prefe_in_sessione)
{
    foreach ($entries_table as $entry) {
        foreach ($prefe_in_sessione as $prodotto_prefe) {
            if ($entry["id"] == $prodotto_prefe) {
                echo "<table>";
                echo "<tbody>";
            
                echo "<form action='togli.php' method='POST'>";
                echo "<tr>";
                echo "<input name='id' value='{$entry['id']}' style='display:none'>"; // lol
                echo "<td>" . $entry["id"] . "</td>";
                echo "<td>" . $entry["Nome"] . "</td>";
                echo "<td>" . $entry["Descrizione"] . "</td>";
                echo "<td>" . $entry["Prezzo"] . "</td>";
                echo "<td>" . "<input type='submit' value='togli dai preferiti'>" . "</td>";
                echo "</form>";
                echo "</tr>";
            
                echo "</tbody>";
                echo "</table>";
            }
        }
    }
}


function main() {
    session_start();

    if (ini_get("session.get_cookies"))
        $params = session_get_cookie_params();

    $conn = get_conn_db(
        "127.0.0.1",
        "db",
        "root",
        ""
    );
    
    $entries_table = do_query($conn);
    $create_new_array = [];

    if (!empty($entries_table)) {
        display_table($entries_table, $_SESSION["preferiti"]);
    } else {
        echo "Empty";
    }
}

main();
exit;
?>