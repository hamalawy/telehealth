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


	    exec('cd /var/www/deviewer/edfviewer/ && python viewer2.py', $edf);
	    $data['ecg'] = $edf[1];
	    $data['patient'] = $edf[0];
	    $data['bp'] = $edf[3];
	    $data['spo2'] = $edf[2];
	    $data['heartrate'] = $edf[4];

            $this->load->view('rxbox/deview', $data);
        }
    }
        
?>
