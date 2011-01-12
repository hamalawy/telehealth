<?php

class Main extends Controller {

	function Main() {
		parent::Controller();	
	}
	
	function index() {
		$data['title'] = "weh";
		$data['script'] = array('hi.js','hello.js');
		$data['css'] = array('hello.css');
		$this->load->view('template', $data);
	}
}

/* End of file main.php */
/* Location: ./system/application/controllers/main.php */