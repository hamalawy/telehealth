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
  <div class="ui-widget ui-corner-all ui-widget-content" style="float: left; width: 20%">
   <p><h2>Cases</h2></p>
   <div  style="margin: 5%;">
	<?php
		$mbox = imap_open("{imap.gmail.com:993/imap/ssl/novalidate-cert}INBOX", "nurse.triage", "telehealth")
		     or die("can't connect: " . imap_last_error());
	
		$MC = imap_check($mbox);

		// Fetch an overview for all messages in INBOX
		$result = imap_search($mbox, 'UNSEEN');
                $result = imap_fetch_overview($mbox,join(',',$result),0);
		foreach ($result as $overview) {
		    echo "#{$overview->msgno} {$overview->subject}<br/>";
		}
		imap_close($mbox);
	?>

   </div>

  </div>

  <div class="ui-widget ui-widget-content ui-corner-all" style="float: right">
<center>
<table width="95%" border="1" style="border-collapse: collapse; margin: 2%">
<tr>
<td height="114" colspan="4"><?php echo $patient; ?></td>
</tr>
<tr>
<td width="23%" height="56">&nbsp;</td>
<td colspan="2">&nbsp;</td>
<td width="30%">&nbsp;</td>
</tr>
<tr>
<td height="329" colspan="3" rowspan="2">
<div id="placeholder" style="width:683px;height:267px;"></div>
</td>
<td height="275">&nbsp;</td>
</tr>
<tr>
<td rowspan="3"><div id="iResp"></div>
      <form name="sendForm" onSubmit="return sendMsg(this);" action="#">
        <div class="spaced"><b>To:</b> <input type="text" name="sendTo" tabindex="1"></div>
        <div class="spaced"><textarea name="msg" id='msgArea' rows="3" cols="80" tabindex="2"></textarea></div>
        <div class="spaced"><input type="submit" value="Send" tabindex="3"> * <input type="button" value="Quit" tabindex="4" onclick="return quit();"></div>
      </form>
</td>
</tr>
<tr>
<td height="23">Blood Pressure</td>
<td width="23%">Heart Rate</td>
<td width="24%">Blood Oxygen Saturation</td>
</tr>
<tr>
<td height="86">
<h1><center><?php echo $bp; ?></center></h1>
</td>
<td>
<h1><center><?php echo $heartrate; ?><br/>BPM</center>
</td>
<td>
<h1><center><?php echo $spo2; ?><br/>%SP02</center>
</td>
</tr>
<tr>
<td colspan="4">&nbsp;</td>
</tr>
</table>
</center>
    </div>
    </div>
<?php $this->load->view('header'); ?>

