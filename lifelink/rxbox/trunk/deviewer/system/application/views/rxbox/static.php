<?php $this->load->view('header'); ?>
<style type="text/css"> 
	/* jQuery lightBox plugin - Gallery style */
	#gallery {
		text-align:left;
		padding: 5px;
	}
	#gallery ul { list-style: none; }
	#gallery ul li { display: inline; }
	#gallery ul img {
		border: 5px solid #D4CCB0;
		border-width: 5px 5px 20px;
	}
	#gallery ul a:hover img {
		border: 5px solid #fff;
		border-width: 5px 5px 20px;
		color: #fff;
	}
	#gallery ul a:hover { color: #fff; }
</style> 

<script type="text/javascript">
$(function() {
	$('#gallery a').lightBox({
	    overlayOpacity: 0.6,
	    imageLoading: '<?php echo base_url() ?>public/lightbox/images/lightbox-ico-loading.gif',
	    imageBtnClose: '<?php echo base_url() ?>public/lightbox/images/lightbox-btn-close.gif',
	    imageBtnPrev: '<?php echo base_url() ?>public/lightbox/images/lightbox-btn-prev.gif',
	    imageBtnNext: '<?php echo base_url() ?>public/lightbox/images/lightbox-btn-next.gif',
   	}); // Select all links in object with gallery ID
});

</script>

<script id="source" language="javascript" type="text/javascript">
function formatter(val, axis){
    if (val == "11.0"){
	return "1.0";
    }
    else return "";
}

$(function () {
    var samples = 7500;
    var frequency = 500;
    var ymin = 16084;
    var ymax = 16684;
    var xmax = 1500;
    var maj_grid_color = "#C0C0C0";
    var grid_bgcolor = "#FFFFFF";

    var placeholder = $("#placeholder");
    var d1 = <?php echo $ecg; ?>;

    var xticks = [];
    for (i=0;i<=samples;i++) {
	if(i%100 == 0) {
		xticks.push([i, (i*.002).toFixed(2)]);
	}
	else if (i%20 ==0) {
		xticks.push([i, ""]);
	}
    }

    var yticks = [];
    for (i=ymin;i<=ymax;i+=20) {
        yticks.push([i, ""]);
    }


    var options = {
	series: {
	    lines: { show: true},
	    shadowSize: 0
	},
	colors: ["#ff0000", "#00ff00", "#000033"],
	grid: {
	    backgroundColor: grid_bgcolor,
	    markings: function (axes) {
	    	var markings =[];
	    	for (var x = Math.floor(axes.xaxis.min); x < samples; x += 100)
	    	      markings.push({ xaxis: { from: x, to: x }, color: maj_grid_color });
                for (var y = Math.floor(axes.yaxis.min); y < axes.yaxis.max; y += 100)
                      markings.push({ yaxis: { from: y, to: y }, color: maj_grid_color });
	    	return markings;
	    }
	},
	xaxis: { position: 'bottom', ticks: xticks, max: xmax, panRange: [0, samples] },
	yaxis: { ticks: yticks, min: ymin, max: ymax, panRange: [ymin, ymax] },
        pan: { interactive: true,  },
    };

    var plot = $.plot(placeholder,  [d1], options);

    //placeholder.bind('plotpan', function (event, plot) {
    //    var axes = plot.getAxes();
    //});


    function addArrow(dir, right, top, offset) {
        $('<img class="button" src="<?php echo base_url() ?>public/images/arrow-' + dir + '.gif" style="position: absolute; right:' + right + 'px;top:' + top + 'px">').appendTo(placeholder).click(function (e) {
            e.preventDefault();
            plot.pan(offset);
        });
    }
 
    addArrow('left', 1050, 10, { left: -plot.width()/15 });
    addArrow('right', 10, 10, { left: plot.width()/15 });

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
   <div style="margin-left: 50px;"><h2><?php echo $subject; ?></h2><h3><?php echo $patient;?></h3><p><?php echo $description; ?></p></div></td>
</tr>
<tr>
<td height="329" colspan="3" rowspan="2" valign="top">
<center><h3 class="ui-corner-all widget-headers ui-widget-header">Electrocardiograph</h3>
<center><div id="placeholder" style="width: 1080px; height: 367px;"></div></center>
</td>
<td height="275" valign="top"><center><h3 class="ui-corner-all widget-headers ui-widget-header">Photos</h3>
<div id="gallery">
                	<ul>
                    	<li>
                        	<a href="<?php echo base_url() ?>public/lightbox/photos/image1.jpg" title="Image a">
                            	<img src="<?php echo base_url() ?>public/lightbox/photos/thumb_image1.jpg" width="72" height="72" alt="">
                            </a>
                        </li>
                    	<li>
                        	<a href="<?php echo base_url() ?>public/lightbox/photos/image2.jpg" title="Image b">
                            	<img src="<?php echo base_url() ?>public/lightbox/photos/thumb_image2.jpg" width="72" height="72" alt="">
                            </a>
                        </li>
                    	<li>
                        	<a href="<?php echo base_url() ?>public/lightbox/photos/image3.jpg" title="Image c">
                            	<img src="<?php echo base_url() ?>public/lightbox/photos/thumb_image3.jpg" width="72" height="72" alt="">
                            </a>
                        </li>
                    	<li>
                        	<a href="<?php echo base_url() ?>public/lightbox/photos/image4.jpg" title="Image d">
                            	<img src="<?php echo base_url() ?>public/lightbox/photos/thumb_image4.jpg" width="72" height="72" alt="">
                            </a>
                        </li>
                        <li>
                        	<a href="<?php echo base_url() ?>public/lightbox/photos/image5.jpg" title="Image e">
                            	<img src="<?php echo base_url() ?>public/lightbox/photos/thumb_image5.jpg" width="72" height="72" alt="">
                            </a>
                        </li>
                    </ul>
                </div>
</td>
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

