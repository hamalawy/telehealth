<?php

class Concept_log extends Model {
    /*
     * Generic functions for accessing the concept_log table.
     */
    function Concept_log()
    {
        parent::Model();
    }
    
    function get_log($id=0)
    {
        /*
         * Returns logs corresponding to the id given. Returns all logs if no id is given.
         */
        if ($id != 0)
            $this->db->where('id', $id);
        return $this->db->get('concept_log')->result();
    }
    
    function _get_curr_value($id, $key)
    {
        /*
         * Returns entry found at the field named 'key' that corresponds to the id given. Table is taken from 'log_table' in the session variables. Returns FALSE if id does not exist.
         */
        $this->db->select($key);
        $log_params = $this->db->get_where($this->session->userdata('log_table'),
                                           array('id' => $id))->row_array();
        if (count($log_params) == 0)
            return FALSE; // nothing to do
        return $log_params[$key];
    }
    
    function _add_log($id, $key, $value, $reason)
    {
        /*
         * Returns last inserted id. Creates a log entry inside the 'log_table' table.
         * 
         * Remember to insert the following lines of code before modifying rows:
         * --code starts here--
         * $log_value = $this->Concept_log->_get_curr_value($id, $key);
         * if ( ($value === FALSE) OR ($value == $log_value))
         *     return; // non-existent entry OR same value
         * --code ends here--
         */
        $log_table = $this->session->userdata('log_table');
        foreach ($this->db->field_data($log_table) as $field)
        {
            if ($field->name != $key)
                continue; // not the required key
            switch ($field->type)
            {
                // get datatype. This determines the table (concept_log_*) where the logs will be placed.
                case "tinyint":
                case "smallint":
                case "mediumint":
                case "int":
                case "bigint":
                case "boolean":
                    $log_table = 'int';
                    break;
                case "char":
                case "varchar":
                case "binary":
                case "varbinary":
                case "blob":
                case "text":
                case "enum":
                case "set":
                case "string":
                case "datetime":
                    $log_table = 'str';
                    break;
            }
            if (isset($log_table) && ($log_table != ''))
                break; // table already determined
        }
        if ( ! $log_table)
            return 0; // nothing to do
        
        $log_id = $this->_add_modified_value('concept_log_' . $log_table, $value);
        
        // get current timestamp
        $this->db->select("NOW()");
        $log_date = $this->db->get()->row_array();
        $log_date = $log_date['NOW()'];
        
        // create log
        $this->db->set('table_name', $this->session->userdata('log_table'));
        $this->db->set('table_id', $id);
        $this->db->set('field_modified', $key);
        $this->db->set('log_table_name', $log_table);
        $this->db->set('modified_by', $this->session->userdata('peers_user'));
        $this->db->set('modify_reason', $reason);
        $this->db->set('log_table_id', $log_id);
        $this->db->set('date_modified', $log_date);
        $this->db->insert('concept_log');
        
        // unset session fields
        $this->session->unset_userdata('log_table');
        return $this->db->insert_id();
    }
    
    function _add_modified_value($table, $value)
    {
        /*
         * Returns last inserted id. Creates a log entry inside the 'concept_log_<datatype>' table. Entry should be of the correct datatype.
         */
        $this->db->set('log_value', $value);
        $this->db->insert($table);
        return $this->db->insert_id();
    }
}
?>