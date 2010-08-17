<?php
    class Rxbox extends Controller {
        function Rxbox()
        {
            parent::Controller();
        }
        function index()
        {
        }
        function session($view='static', $q='')
        {
	    $data['sent']=false;

            $data['title'] = "Domain Expert's Window";
            $data['extraHeadContent'] =
                array(
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.js"></script>',
                    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.flot.js"></script>',
		    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.flot.image.js"></script>',
		    '<script type="text/javascript" src="' . base_url() . 'public/js/flot/jquery.flot.navigate.js"></script>',
		    '<script type="text/javascript" src="' . base_url() . 'public/lightbox/jquery.lightbox-0.5.js"></script>',
		    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/lightbox/css/jquery.lightbox-0.5.css" media="screen" />',
		    //'<script type="text/javascript" src="' . base_url() . 'public/js/jsjac-1.3.2/jsjac.js"></script>',
		    //'<script type="text/javascript" src="' . base_url() . 'public/js/chat.js"></script>',
		    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/jquery-ui/css/south-street/jquery-ui.css"></link>',
		    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/css/deview.css"></link>'
                 );



	    //If Attachment found
            $data['ecg'] = "[[0,0]]";
            $data['patient'] = "---";
            $data['bp'] = "---";
            $data['spo2'] = "---";
            $data['heartrate'] = "---";
	    $data['subject'] = "---";
            $data['description'] = "---";


            $this->load->model('attachment_model');
            $attachments = $this->attachment_model->getAttachmentsByHash($q);
	    $data['subject'] = $this->attachment_model->getSubject($attachments[0]->msg_uuid);
	    $data['description'] = $this->attachment_model->getBody($attachments[0]->msg_uuid);
	
	    //FIXME: 
	    //$data['from'] = $this->attachment_model->getFrom($attachments[0]->msg_uuid);
	    $data['from'] = 'dttb.rxbox@gmail.com';

	    //TODO: Check file extension first

	    $filename = $this->writeToTempFile($attachments[0]->content);
	

	    //Message id
	    $data['q'] = $q;
	    $data['view'] = $view;

	    exec('cd /home/jerome/public_html/deviewer/edfviewer && python viewer2.py ' . $filename, $edf);
            $data['ecg'] = $edf[1];
            $data['patient'] = $edf[0];
            $data['bp'] = $edf[3];
            $data['spo2'] = $edf[2];
            $data['heartrate'] = $edf[4];


	    #delete temporary file
	    unlink($filename);

            if (!empty($_POST['msg'])) {
                $data['msg'] = $_POST['msg'];
                $data['sent'] = $this->attachment_model->setReply($attachments[0]->msg_uuid, $data['subject'], $data['msg'], $data['from'], 'de.hospital@gmail.com');
            }


            $this->load->view("rxbox/$view", $data);

        }

	function writeToTempFile($attachment) {
		$tmpfilename = "/tmp/" . md5(date('U') . mt_rand()) . ".edf";
		$fh = fopen($tmpfilename, 'wb') or die("can't open file");
		fwrite($fh, $attachment);
		fclose($fh);

		return $tmpfilename;
	}
    }
        
?>
