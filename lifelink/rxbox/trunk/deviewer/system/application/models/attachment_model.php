<?php
class Attachment_model extends Model {

    function Attachment_model()
    {
        parent::Model();
    }
    
    function getAttachmentsByHash($hash)
    {
	$query = $this->db->get_where('hash_table', array('hash_key' => $hash));

	//TODO: Verify if result < 0
	$result = $query->result();
	$msg_uuid = $result[0]->msg_id;

	$query = $this->db->get_where('msg_attachments', array('msg_uuid' => $msg_uuid));			
	if ($query->num_rows() <= 0)
	{
	}else{
		return $query->result();
	}
    }


}
?>

