<?php

$debug = 1;

if ($debug) {
    ini_set("display_errors", 1);
    error_reporting(E_ALL);    
}

// echo $_SERVER["REQUEST_METHOD"];
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    echo "method not allowed!<br>";
    exit;
}

session_start();

if (!isset($_SESSION["preferiti"]))
    $_SESSION["preferiti"] = array();

if (ini_get("session.get_cookies")) {
    $params = session_get_cookie_params();
}

function check_if_in_array($array, $new_element) {
    foreach ($array as $entry)
        if ($entry == $new_element)
            return 0;
    return 1;
}

if (check_if_in_array($_SESSION["preferiti"], $_POST["id"])) {
    $_SESSION["preferiti"][] = $_POST["id"];
}

header("Location: index.php");
exit;

?>