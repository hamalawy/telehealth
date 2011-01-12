<?php if(isset($title)) echo "<title>" . $title . "</title>\n";?>

<!-- Add user-defined scripts -->
<script src='/jquery-1.4.2.min.js'></script>
<?php
	if(!isset($script)) $script=array();
	foreach($script as $item) echo "<script src='" . $item . "'></script>\n";
	if(!isset($css)) $css=array();
	foreach($css as $item) echo "<link rel='stylesheet' type='text/css' href='" . $item . "' />\n";
?>