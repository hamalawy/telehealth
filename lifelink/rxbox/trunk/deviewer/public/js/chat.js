function handleIQ(aIQ) {
  document.getElementById('iResp').innerHTML += 
    "<div class='msg'>IN (raw): " +aIQ.xml().htmlEnc() + '</div>';
  document.getElementById('iResp').lastChild.scrollIntoView();
  con.send(aIQ.errorReply(ERR_FEATURE_NOT_IMPLEMENTED));
}

function handleMessage(aJSJaCPacket) {
  var html = '';
  html += '<div class="msg"><b>Received Message from '+aJSJaCPacket.getFromJID()+':</b><br/>';
  html += aJSJaCPacket.getBody().htmlEnc() + '</div>';
  document.getElementById('iResp').innerHTML += html;
  document.getElementById('iResp').lastChild.scrollIntoView();
}

function handlePresence(aJSJaCPacket) {
  var html = '<div class="msg">';
  if (!aJSJaCPacket.getType() && !aJSJaCPacket.getShow()) 
    html += '<b>'+aJSJaCPacket.getFromJID()+' has become available.</b>';
  else {
    html += '<b>'+aJSJaCPacket.getFromJID()+' has set his presence to ';
    if (aJSJaCPacket.getType())
      html += aJSJaCPacket.getType() + '.</b>';
    else
      html += aJSJaCPacket.getShow() + '.</b>';
    if (aJSJaCPacket.getStatus())
      html += ' ('+aJSJaCPacket.getStatus().htmlEnc()+')';
  }
  html += '</div>';

  document.getElementById('iResp').innerHTML += html;
  document.getElementById('iResp').lastChild.scrollIntoView();
}

function handleError(e) {
  document.getElementById('err').innerHTML = "An error occured:<br />"+ 
    ("Code: "+e.getAttribute('code')+"\nType: "+e.getAttribute('type')+
    "\nCondition: "+e.firstChild.nodeName).htmlEnc(); 
  document.getElementById('login_pane').style.display = '';
  document.getElementById('sendmsg_pane').style.display = 'none';
  
  if (con.connected())
    con.disconnect();
}

function handleStatusChanged(status) {
  oDbg.log("status changed: "+status);
}

function handleConnected() {
  document.getElementById('login_pane').style.display = 'none';
  document.getElementById('sendmsg_pane').style.display = '';
  document.getElementById('err').innerHTML = '';

  con.send(new JSJaCPresence());
}

function handleDisconnected() {
  document.getElementById('login_pane').style.display = '';
  document.getElementById('sendmsg_pane').style.display = 'none';
}

function handleIqVersion(iq) {
  con.send(iq.reply([
                     iq.buildNode('name', 'jsjac simpleclient'),
                     iq.buildNode('version', JSJaC.Version),
                     iq.buildNode('os', navigator.userAgent)
                     ]));
  return true;
}

function handleIqTime(iq) {
  var now = new Date();
  con.send(iq.reply([iq.buildNode('display',
                                  now.toLocaleString()),
                     iq.buildNode('utc',
                                  now.jabberDate()),
                     iq.buildNode('tz',
                                  now.toLocaleString().substring(now.toLocaleString().lastIndexOf(' ')+1))
                     ]));
  return true;
}

function doLogin(aForm) {
  document.getElementById('err').innerHTML = ''; // reset

  try {
    // setup args for contructor
    oArgs = new Object();
    oArgs.httpbase = aForm.http_base.value;
    oArgs.timerval = 2000;

    if (typeof(oDbg) != 'undefined')
      oArgs.oDbg = oDbg;

    if (aForm.backend[0].checked)
      con = new JSJaCHttpBindingConnection(oArgs);
    else
      con = new JSJaCHttpPollingConnection(oArgs);

    setupCon(con);

    // setup args for connect method
    oArgs = new Object();
    oArgs.domain = aForm.server.value;
    oArgs.username = aForm.username.value;
    oArgs.resource = 'jsjac_simpleclient';
    oArgs.pass = aForm.password.value;
    oArgs.register = aForm.register.checked;
    oArgs.authtype = 'nonsasl';
    con.connect(oArgs);
  } catch (e) {
    document.getElementById('err').innerHTML = e.toString();
  } finally {
    return false;
  }
}

function setupCon(con) {
    con.registerHandler('message',handleMessage);
    con.registerHandler('presence',handlePresence);
    con.registerHandler('iq',handleIQ);
    con.registerHandler('onconnect',handleConnected);
    con.registerHandler('onerror',handleError);
    con.registerHandler('status_changed',handleStatusChanged);
    con.registerHandler('ondisconnect',handleDisconnected);

    con.registerIQGet('query', NS_VERSION, handleIqVersion);
    con.registerIQGet('query', NS_TIME, handleIqTime);
}

function sendMsg(aForm) {
  if (aForm.msg.value == '' || aForm.sendTo.value == '')
    return false;

  if (aForm.sendTo.value.indexOf('@') == -1)
    aForm.sendTo.value += '@' + con.domain;

  try {
    var aMsg = new JSJaCMessage();
    aMsg.setTo(new JSJaCJID(aForm.sendTo.value));
    aMsg.setBody(aForm.msg.value);
    con.send(aMsg);

    aForm.msg.value = '';

    return false;
  } catch (e) {
    html = "<div class='msg error''>Error: "+e.message+"</div>"; 
    document.getElementById('iResp').innerHTML += html;
    document.getElementById('iResp').lastChild.scrollIntoView();
    return false;
  }
}

function quit() {
  var p = new JSJaCPresence();
  p.setType("unavailable");
  con.send(p);
  con.disconnect();

  document.getElementById('login_pane').style.display = '';
  document.getElementById('sendmsg_pane').style.display = 'none';
}

function init() {
  if (typeof(Debugger) == 'function') {
    oDbg = new Debugger(2,'simpleclient');
    oDbg.start();
  } else {
    // if you're using firebug or safari, use this for debugging
    //oDbg = new JSJaCConsoleLogger(2);
    // comment in above and remove comments below if you don't need debugging
    oDbg = function() {};
    oDbg.log = function() {};
  }


  try { // try to resume a session
    if (JSJaCCookie.read('btype').getValue() == 'binding')
      con = new JSJaCHttpBindingConnection({'oDbg':oDbg});
    else
      con = new JSJaCHttpPollingConnection({'oDbg':oDbg});

    setupCon(con);

    if (con.resume()) {

      document.getElementById('login_pane').style.display = 'none';
      document.getElementById('sendmsg_pane').style.display = '';
      document.getElementById('err').innerHTML = '';

    }
  } catch (e) {} // reading cookie failed - never mind

}
onload = init;

onerror = function(e) { 
  document.getElementById('err').innerHTML = e; 

  document.getElementById('login_pane').style.display = '';
  document.getElementById('sendmsg_pane').style.display = 'none';

  if (con && con.connected())
    con.disconnect();
  return false; 
};

onunload = function() {
  if (typeof con != 'undefined' && con && con.connected()) {
  // save backend type
    if (con._hold) // must be binding
      (new JSJaCCookie('btype','binding')).write();
    else
      (new JSJaCCookie('btype','polling')).write();
    if (con.suspend) {
      con.suspend(); 
    }
  }
};

