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
                    '<link rel="stylesheet" type="text/css" href="' . base_url() . 'public/css/triageviewer.css"></link>'
                 );
            $this->load->view('rxbox/session', $data);
        }
    }
        
?>