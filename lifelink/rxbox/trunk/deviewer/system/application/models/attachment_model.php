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

    function getFrom($msg_uuid)
    {
	$query = $this->db->get_where('msg_headers', array('msg_uuid' => $msg_uuid, 'field' => 'from'));
        $result = $query->result();
        return $result[0]->value;
    }

    function getSubject($msg_uuid)
    {
        $query = $this->db->get_where('msg_headers', array('msg_uuid' => $msg_uuid, 'field' => 'subject'));
        $result = $query->result();
        return $result[0]->value;
    }

    function getBody($msg_uuid)
    {
	$query = $this->db->get_where('msg_contents', array('msg_uuid' => $msg_uuid));
	$result = $query->result();
	return $result[0]->body;
    }

    function setReply($msg_uuid, $subject, $reply, $receiver, $de_email)
    {
	$content = "<msg><headers subject='$subject' from='$de_email' to='$receiver'/><content contact='$receiver' text_content='$reply'/><attachments /></msg>";
	$data = array(
		'msg_uuid'=> $msg_uuid,
		'receiver'=> $receiver,
		'content' => $content,
		'mode' => 'triage',
		'module' => 'buddyworks',
		'date_sent' => date("Y-m-d H:i:s")
		);
	$query = $this->db->insert('msg_outgoing', $data);
/*
	echo "<pre>";
	print_r($data);
	echo "</pre>";
*/
    }

}
?>

