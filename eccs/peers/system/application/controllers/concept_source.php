<?php

class Concept_source extends Controller {
    /*
     * Functions for accessing concept source table.
     */
    function __construct()
    {
        parent::Controller();
        $this->load->model('Concept_log');
    }
    
    function index($value, $reason)
    {
        // do nothing
    }
    
    function get($id=0)
    {
        /*
         *  No return value. Prints concept sources as json-encoded strings.
         */
        if ($id != 0)
            $this->db->where('id', $id);
        echo json_encode($this->db->get('concept_source')->result());
    }
    
    function search($value)
    {
        /*
         *  No return value. Prints matching concept sources as json-encoded strings. Fields to be searched are the 'name' and 'citation' columns. String matching is done using regular expressions.
         */
        $query = "(SELECT `id`,'name' AS `field`,`name` AS `content` from `concept_source` where `name` REGEXP '$value') UNION (SELECT `id`,'citation' AS `citation`,`citation` AS `content` from `concept_source` where `citation` REGEXP '$value')";
        
        echo json_encode($this->db->query($query)->result());
    }
    
    function add($source_name, $source_citation='')
    {
        /*
         *  Returns last inserted id. Creates a new concept source entry.
         */
        // get current timestamp
        $this->db->select("NOW()");
        $insert_date = $this->db->get()->row_array();
        $insert_date = $insert_date['NOW()'];
        
        // replace value
        if ($source_citation)
        {
            $this->db->set('citation', $source_citation);
        }
        $this->db->set('name', $source_name);
        $this->db->set('created_by', $this->session->userdata('peers_user'));
        $this->db->set('date_created', $insert_date);
        $this->db->insert('concept_source');
        
        return $this->db->insert_id();
    }
    
    function void($id, $reason)
    {
        /*
         *  Returns output of the edit() function. Voids a concept source.
         */
        return $this->edit($id, 'voided', 1, $reason);
    }
    
    function edit($id, $key, $value, $reason='')
    {
        /*
         *  No return value. Modifies row contents corresponding to the id given. Creates a log entry afterwards. Exits when id does not exist or when modifying value is the same as the current value.
         */
        $this->session->set_userdata('log_table', 'concept_source');
        
        $log_value = $this->Concept_log->_get_curr_value($id, $key);
        if ( ($value === FALSE) OR ($value == $log_value))
            return; // non-existent entry OR same value
        
        // replace value
        $this->db->set($key, $value);
        $this->db->where('id', $id);
        $this->db->update('concept_source');
        
        // update log
        $this->Concept_log->_add_log($id, $key, $log_value, $reason);
    }
    
}
