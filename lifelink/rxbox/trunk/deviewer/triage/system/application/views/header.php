<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></meta>

<?php
    if (isset($title)) { echo "<title>" . $title . "</title>\n"; }

    if (isset($extraHeadContent)) {
        if ( (is_array($extraHeadContent)) && (!empty($extraHeadContent)) ) {
            foreach($extraHeadContent as $tmpnr => $toshow) { echo $toshow . "\n"; }
        } else { echo $extraHeadContent; }
    }
?>

</head>
<body>
<noscript><p>Your browser either does not support JavaScript, or you have JavaScript turned off.</p></noscript>