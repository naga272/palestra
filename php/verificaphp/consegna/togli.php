<a href="index.php">homepage</a>
<br>

<?php

$debug = 1;

if ($debug) {
    ini_set("display_errors", 1);
    error_reporting(E_ALL);    
}


function check_if_in_array($array, $new_element)
{
    foreach ($array as $entry)
        if ($entry == $new_element)
            return 0;
    return 1;
}


function togli_from_array($array, $id)
{
    $new_array = array(); 
    foreach ($array as $value)
        if ($id != $value)
            $new_array[] = $value;

    return $new_array;
}


function main()
{
    // echo $_SERVER["REQUEST_METHOD"];
    if ($_SERVER["REQUEST_METHOD"] !== "POST") {
        echo "method not allowed!<br>";
        exit;
    }

    session_start();

    if (ini_get("session.get_cookies"))
        $params = session_get_cookie_params();

    $_SESSION["preferiti"] = togli_from_array($_SESSION["preferiti"], $_POST["id"]);

    header("Location: preferiti.php");
    exit;
}

main();
?>