<?php

$link = mysql_connect("localhost","root","root") or die ("Unable to connect to SQL server");
mysql_select_db("test_edf",$link) or die ("Unable to select database");

//$datapath = "/var/www/uploads/" . $_GET['session'] . "/current";

//$file_handle = fopen($datapath, "r");
//if ($file_handle == NULL) die;

//$data = $lead1 = $lead2 = array();

/*while (!feof($file_handle) ) {
	$line = fgets($file_handle, 1024);
	if (preg_match("/\d+\:(\d+\.\d+)\s+([-\.\d]+)\s+([-\.\d]+)/", $line, $res)) {
		array_shift($res);

		$res[0] = floatval($res[0]);
		$res[1] = floatval($res[1]);
		$res[2] = floatval($res[2]);

		$lead1[] = array($res[0], $res[1]);
		$lead2[] = array($res[0], $res[2]);
	}
}
$data = array($lead1, $lead2);
fclose($file_handle);
*/
    
header("Content-type: text/plain");
//echo json_encode($data);
    $data = mysql_query('SELECT val FROM edfs where id=4');
    if (!$result) die;
    echo $data;
?>
