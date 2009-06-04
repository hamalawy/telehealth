<?php
$FUP = $_FILES["file"];
if ($FUP["error"] > 0) {
    echo "Error: " . $FUP["error"]  . "<br />";
}
else {
    echo "Upload: " . $FUP["name"] . "<br />";
    echo "Type: " . $FUP["type"] . "<br />";
    echo "Size: " . $FUP["size"] . "<br />";
    echo "Location: " . $FUP["tmp_name"] . "<br />";
}
?>
