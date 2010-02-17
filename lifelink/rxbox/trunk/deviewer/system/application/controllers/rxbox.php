<?php
    class Rxbox extends Controller {
        function Rxbox()
        {
            parent::Controller();
        }
        function index()
        {
        }
        function session($q='')
        {
            $data['title'] = "Domain Expert's Window";
            $data['extraHeadContent'] =
                array(
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.js"></script>',
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.flot.js"></script>',
		    '<script type="text/javascript" src="' . base_url() . 'public/js/jsjac-1.3.2/jsjac.js"></script>',
		    '<script type="text/javascript" src="' . base_url() . 'public/js/chat.js"></script>',
		    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/jquery-ui/css/south-street/jquery-ui.css"></link>',
		    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/css/deview.css"></link>'
                 );


	    $username = "nurse.triage";
            $mbox = imap_open("{imap.gmail.com:993/imap/ssl/novalidate-cert}INBOX", "nurse.triage", "telehealth")
                     or die("can't connect: " . imap_last_error());

	    #This code assumes that there is only one edf file attachent - to be fixed
	    $data['unread'] = $this->_get_mails($mbox, 'UNSEEN');
	    $attachment = $this->_extract_attachments($mbox, $q);
	    $filename = "";
	    foreach ($attachment as $a) {
		if($a['is_attachment'] == true) {
			$filename = "/tmp/". md5($a['filename'] . date('U') . $username) . ".edf";
			$fd = fopen($filename, 'wb');
			fwrite($fd, $a['attachment']);
			fclose($fd);
			break;
		}
	    }

	    //If Attachment found
            $data['ecg'] = "[[0,0]]";
            $data['patient'] = "---";
            $data['bp'] = "---";
            $data['spo2'] = "---";
            $data['heartrate'] = "---";

	    if ($filename != "") {
	            exec('cd /var/www/deviewer/edfviewer/ && python viewer2.py ' . $filename, $edf);

		    #delete temporary file
		    unlink($filename);

	            $data['ecg'] = $edf[1];
	            $data['patient'] = $edf[0];
	            $data['bp'] = $edf[3];
	            $data['spo2'] = $edf[2];
	            $data['heartrate'] = $edf[4];
	    }

	    $data['description'] = $this->_get_body($mbox, $q);
            $this->load->view('rxbox/deview', $data);

            imap_close($mbox);
        }

	function _get_mails($mbox, $search ) {
                $MC = imap_check($mbox);

                $result = imap_search($mbox, $search);
                $result = imap_fetch_overview($mbox,join(',',$result),0);

		return array_reverse($result);
	}

	function _get_body($mbox, $uid) {
		$body = imap_fetchbody($mbox, $uid, 1);
		return $body;
	}

	function _extract_attachments($connection, $message_number) {
   
	    $attachments = array();
	    $structure = imap_fetchstructure($connection, $message_number);
	    if(isset($structure->parts) && count($structure->parts)) {
   
	        for($i = 0; $i < count($structure->parts); $i++) {
   
	            $attachments[$i] = array(
	                'is_attachment' => false,
	                'filename' => '',
	                'name' => '',
	                'attachment' => ''
        	    );
           
	            if($structure->parts[$i]->ifdparameters) {
	                foreach($structure->parts[$i]->dparameters as $object) {
	                    if(strtolower($object->attribute) == 'filename') {
	                        $attachments[$i]['is_attachment'] = true;
	                        $attachments[$i]['filename'] = $object->value;
	                    }
	                }
	            }
           
	            if($structure->parts[$i]->ifparameters) {
	                foreach($structure->parts[$i]->parameters as $object) {
	                    if(strtolower($object->attribute) == 'name') {
	                        $attachments[$i]['is_attachment'] = true;
	                        $attachments[$i]['name'] = $object->value;
	                    }
	                }
	            }
	           
	            if($attachments[$i]['is_attachment']) {
	                $attachments[$i]['attachment'] = imap_fetchbody($connection, $message_number, $i+1);
	                if($structure->parts[$i]->encoding == 3) { // 3 = BASE64
	                    $attachments[$i]['attachment'] = base64_decode($attachments[$i]['attachment']);
	                }
	                elseif($structure->parts[$i]->encoding == 4) { // 4 = QUOTED-PRINTABLE
	                    $attachments[$i]['attachment'] = quoted_printable_decode($attachments[$i]['attachment']);
	                }
	            }
        	   
	        }
	       
	    }
   
	    return $attachments;
   
	}


    }
        
?>
