<?php
    include("../../_path.php");
    $uuid = '5982f5a0-b71e-11de-9ad3-0013724f08d6';
    $edf = `python $MHPATH/modules/_main/code/runner.py -c :main buddyworks:edf $uuid`;
    echo $edf;
?>
