<?php $this->load->view('header'); ?>

<script id="source" language="javascript" type="text/javascript">
$(function () {
    var d1 = <?php echo $ecg; ?>;
    $.plot($("#placeholder"), [d1]);
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

  <?php //<div id="sendmsg_pane" style="display:none;"> ?>
  <div>
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

  <div class="ui-widget ui-widget-content ui-corner-all" style="float: right">
  <center><h2 class="widget-headers ui-widget-header ui-corner-all">Rx Panel</h2></center>

<center>
<table width="95%" border="1" style="border-collapse: collapse; margin: 2%; border:1px solid #DFD9C3;">
<tr>
<td height="114" colspan="4" valign="top">
   <center><h3 class="widget-headers ui-widget-header">Patient and Referral Information</h3></center>
   <h2><?php echo $subject; ?></h2><h3><?php echo $patient;?></h3><p><?php echo $description; ?></p></td>
</tr>
<tr>
<td height="329" colspan="3" rowspan="2">
<center><h3 class="widget-headers ui-widget-header">Electrocardiograph</h3>
<center><div id="placeholder" style="width:57em;height:26em;"></div></center>
</td>
<td height="275" valign="top"><center><h3 class="widget-headers ui-widget-header">Photos</h3></td>
</tr>
<tr>
<td rowspan="3" valign="top"><div id="iResp"></div>
      <center><h3 class="ui-widget-header widget-headers">Reply</h3></center>
      <form name="sendForm" onSubmit="return sendMsg(this);" action="#">
        <div class="spaced"><textarea name="msg" id='msgArea' rows="8" cols="80" tabindex="2"></textarea></div>
        <center><div class="spaced"><button type="button" class="ui-state-default ui-corner-all">Send</button></div></center>
      </form>
</td>
</tr>
<tr>
<td width="23%"><center><h3 class="widget-headers ui-widget-header">Blood Pressure</h3></center></td>
<td width="23%"><center><h3 class="widget-headers ui-widget-header">Heart Rate</h3></center></td>
<td width="24%"><center><h3 class="widget-headers ui-widget-header">Blood Oxygen Saturation</h3></center></td>
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
    </div>
<?php $this->load->view('header'); ?>

