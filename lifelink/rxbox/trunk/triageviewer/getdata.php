<?php

$link = mysql_connect("localhost","root","telemedicine311") or die ("Unable to connect to SQL server");
mysql_select_db("test_edf",$link) or die ("Unable to select database");

header("Content-type: text/plain");
    $data = mysql_query('SELECT val FROM edfs where id=4');
    if (!$data) die;
    $x = mysql_fetch_assoc($data);
    echo $x['val'];
?>
