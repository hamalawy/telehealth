<?php $this->load->view('header'); ?>
<script id="source" language="javascript" type="text/javascript">
function formatter(val, axis){
    if (val == "11.0"){
	return "1.0";
    }
    else return "";
}

$(function () {
    var placeholder = $("#placeholder");
    var d1 = <?php echo $ecg; ?>;

    var ticks = [];
    for (i=0;i<=7500;i++) {
	if(i%500 == 0) {
		ticks.push([i, Math.floor(i * .002)]);
	}
	else if (i%20 ==0) {
		ticks.push([i, ""]);
	}
   }


    var options = {
	color: "rgb(255, 0, 0)",
	xaxis: { ticks: ticks, max: 1500, panRange: [0, 7500] },
	yaxis: { min: 16084, max: 16684, panRange: [16084, 16684]  },
	shadowSize: 0,
        pan: {
            interactive: true
        }
    };

    var plot = $.plot(placeholder,  [d1], options);

    function addArrow(dir, right, top, offset) {
        $('<img class="button" src="<?php echo base_url() ?>public/images/arrow-' + dir + '.gif" style="position: absolute; right:' + right + 'px;top:' + top + 'px">').appendTo(placeholder).click(function (e) {
            e.preventDefault();
            plot.pan(offset);
        });
    }
 
    addArrow('left', 1020, 10, { left: -50 });
    addArrow('right', 10, 10, { left: 50 });

});
</script>

  <div id="err"></div>

<?php 
// Disable while designing viewer itseelff
/*  <div id="login_pane">
    <h2>Login</h2>
    <form name="loginForm" onSubmit="return doLogin(this);" action="#">
      <table>
	<tr><th>Backend Type</th><td><input type="radio" name="backend" value="binding" id="backend1" tabindex="1"/> <label for="backend1">HTTP Binding</label><br /> <input type="radio" name="backend" value="polling" id="backend2" tabindex="2"/> <label for="backend2">HTTP Polling</label></td></tr>
	<tr><th><label for="http_base">HTTP Base</label></th><td><input type="text" name="http_base" id="http_base" tabindex="3"/></td></tr>
        <tr><th colspan="2"><hr noshade size="1"/></th></tr>
	<tr><th><label for="server">Jabber Server</label></th><td><input type="text" name="server" id="server" tabindex="4"/></td></tr>
	<tr><th><label for="username">Username</label></th><td><input type="text" name="username" id="username" tabindex="5"/></td></tr>
	<tr><th><label for="password">Password</label></th><td><input type="password" name="password" id="password" tabindex="6" /></td></tr>
	<tr><th></th><td><input type="checkbox" name="register" id="register_checkbox" /> <label for="register_checkbox">Register new account</label></td></tr>
	<tr><td>&nbsp;</td><td><input type="submit" value="Login" tabindex="7"></td></tr>
     </table>
    </form>
  </div>
*/ ?>

<?php if($sent):?>
<div class="ui-widget">
<div style="padding: 0pt 0em; margin-top: 20px;" class="ui-state-highlight ui-corner-all">
                                <p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-info"></span>
                                <strong>Reply sent to triage!</strong></p>
</div>
</div>
<br/>
<?php endif;?>


  <?php //<div id="sendmsg_pane" style="display:none;"> ?>
  <div>
<?php /*
  <div class="ui-corner-all ui-widget-content" style="float: left; height: 61.5em;">
   <center><h2 class="widget-headers ui-widget-header ui-corner-all">Cases</h2></center>
   <div style="margin: 5%">
	<?php
		$subject = '';
		foreach ($unread as $overview) {
		    echo '<a href="' . base_url() . "index.php/rxbox/session/$view/" . $overview->msgno .'">' . $overview->subject . '</a><br/>';
		    if ($overview->msgno == $q) $subject = $overview->subject;
		}
	?>

   </div>

  </div>
*/ ?>
<center>
<table width="98%" border="1" class="ui-widget ui-widget-content" style="border-collapse: collapse; border:1px solid #DFD9C3;">
<tr>
<td height="114" colspan="4" valign="top">
   <center><h3 class="widget-headers ui-widget-header ui-corner-all">Patient and Referral Information</h3></center>
   <h2><?php echo $subject; ?></h2><h3><?php echo $patient;?></h3><p><?php echo $description; ?></p></td>
</tr>
<tr>
<td height="329" colspan="3" rowspan="2" valign="top">
<center><h3 class="ui-corner-all widget-headers ui-widget-header">Electrocardiograph</h3>
<center><div id="placeholder" style="width: 1080px; height: 367px;"></div></center>
</td>
<td height="275" valign="top"><center><h3 class="ui-corner-all widget-headers ui-widget-header">Photos</h3></td>
</tr>
<tr>
<td rowspan="3" valign="top">
      <center><h3 class="ui-corner-all ui-widget-header widget-headers">Reply</h3></center>
      <form name="replyForm" method="post" action="<?php echo current_url(); ?>">
        <div class="spaced"><textarea name="msg" id='msgArea' rows="8" cols="70" tabindex="2" <?php if (!empty($msg)) echo "value='$msg'";?>></textarea></div>
        <center><div class="spaced"><button type="submit" class="ui-state-default ui-corner-all">Send</button></div></center><br/>
      </form>
</td>
</tr>
<tr>
<td width="23%"><center><h3 class="ui-corner-all widget-headers ui-widget-header">Blood Pressure</h3></center></td>
<td width="23%"><center><h3 class="ui-corner-all widget-headers ui-widget-header">Heart Rate</h3></center></td>
<td width="24%"><center><h3 class="ui-corner-all widget-headers ui-widget-header">Blood Oxygen Saturation</h3></center></td>
</tr>
<tr>
<td height="86">
<h1><center><?php echo $bp; ?><br/>mmHg</center></h1>
</td>
<td>
<h1><center><?php echo $heartrate; ?><br/>BPM</center>
</td>
<td>
<h1><center><?php echo $spo2; ?><br/>%SP02</center>
</td>
</tr>
</table>
</center>
    </div>

<?php $this->load->view('footer'); ?>

