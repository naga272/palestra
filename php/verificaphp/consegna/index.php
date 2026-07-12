Welcome!<br>

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



function display_table($entries)
{
    echo "<table>";
    echo "<tbody>";
    
    foreach ($entries as $entry) {
        echo "<form action='aggiungi.php' method='POST'>";
        echo "<tr>";
        echo "<input name='id' value='{$entry['id']}' style='display:none'>"; // lol
        echo "<td>" . $entry["id"] . "</td>";
        echo "<td>" . $entry["Nome"] . "</td>";
        echo "<td>" . $entry["Descrizione"] . "</td>";
        echo "<td>" . $entry["Prezzo"] . "</td>";
        echo "<td>" . "<input type='submit' value='aggiungi ai preferiti'>" . "</td>";
        echo "</form>";
        echo "</tr>";
    }

    echo "</tbody>";
    echo "</table>";
}


function main()
{
    $conn = get_conn_db(
        "127.0.0.1",
        "db",
        "root",
        ""
    );

    $entries = do_query($conn);
    if (!$entries) {
        echo "table is empty";
        exit;
    }

    display_table($entries);

    echo "<a href='preferiti.php'>preferiti</a>";
}


main();
?>