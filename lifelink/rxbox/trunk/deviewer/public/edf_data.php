<?php
    include("../../_path.php");
    $uuid = $_GET['q'];
    $edf = `python $MHPATH/modules/_main/code/runner.py -c :main buddyworks:edf $uuid`;
    echo $edf;
?>