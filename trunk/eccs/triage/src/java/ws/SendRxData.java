/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import javax.xml.ws.soap.*;
import java.sql.*;
import com.sun.xml.ws.developer.*;
import java.io.*;
import javax.xml.bind.annotation.*;
import javax.activation.*;
/**
 *
 * @author User
 */

@WebService(
            name = "SendR",
            serviceName = "SendRxDataService",
            portName = "SendRxDataPort")
public class SendRxData {
    
    private String errormsg = "";
    private String hasNullValue;
    private boolean newmsg = false;
    private String timestamp;

    private DocUser doctor = new DocUser();
    
    public static Date getCurrentJavaSqlDate() {
        java.util.Date today = new java.util.Date();
        return new java.sql.Date(today.getTime());
    }
    
    public boolean hasNullValue(String userkey, String patientid, String firstname, String middlename, 
            String lastname, String sex, int age, String agevalidity, String location) 
    {
        if (userkey.equals("")) {
            hasNullValue = "userkey";
            return true;
        }
        if (patientid.equals("")) {
            hasNullValue = "patientid";
            return true;
        }
        if (firstname.equals("")) {
            hasNullValue = "firstname";
            return true;
        }
        if (middlename.equals("")) {
            hasNullValue = "middlename";
            return true;
        }
        if (lastname.equals("")) {
            hasNullValue = "lastname";
            return true;
        }
        if (sex.equals("")) {
            hasNullValue = "sex";
            return true;
        }
        if (agevalidity.equals("")) {
            hasNullValue = "agevalidity";
            return true;
        }
        if (location.equals("")) {
            hasNullValue = "location";
            return true;
        }
        
        return false;
    }
  
    @WebMethod()
    @WebResult(name="result")
    public boolean newCreatemsg() {
        return this.newmsg;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getCreatemsg() {
        
        String message;
        
        message = this.errormsg;
        
        this.errormsg = "";
        
        this.newmsg = false;
        
        return message;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean sendRxData(@WebParam(name="userkey") String userkey, @WebParam(name="referralid") int referralid, 
            @WebParam(name="ecgtime") String ecgtime, @WebParam(name="ecgy") String ecgy, @WebParam(name="bloodox") double bloodox, @WebParam(name="bpressureu") double bpressureu,
            @WebParam(name="bpressured") double bpressured, @WebParam(name="heartrate") double heartrate, @WebParam(name="ecgsize") int ecgsize, @WebParam(name="timestamp") String timestamp)
    {        
        
 /*       if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
    
    String status = "saved";
    String referrer = this.doctor.getUser();
  
  */
    
    boolean toReturn = true;
    SqlNet connect = new SqlNet();
    int x=0;
        
    
    
  /*      if (hasNullValue(userkey, patientid, firstname, middlename, lastname, sex, age, agevalidity, location)) {
            errormsg = new String("CREATE PATIENT ERROR: Please Fill-Out the REQUIRED Field " + hasNullValue + ".");
            System.err.println(errormsg);
            newmsg = true;
            return false;
        }*/
   /*     long timestamp = ecgtime[1] * 1000;  // msec
        java.util.Date d = new java.util.Date(timestamp);
        java.sql.Date time = new java.sql.Date(d.getTime());*/
        String sql;
        String delims = "[,]";
        String[] tokentime = ecgtime.split(delims);
        String[] tokeny = ecgy.split(delims);
        
        int dataid;
        
        dataid = 434324;
        
        sql = new String("INSERT INTO triage.rxdata" +
                 "(referralid, bloodox, bpressureu, bpressured, heartrate, timestamp ) " +
                 "VALUES (" + referralid + ", " +
                 bloodox + ", " + bpressureu + ", " + bpressured + ", " +
                 heartrate + ", '" + timestamp + "');");
        
        connect.queryUpdate(sql);
        
        while (x < ecgsize) {
                sql = new String("INSERT INTO triage.ecgdata" +
                 "(ecgtime, ecgy, referralid, dataid) " +
                 "VALUES (" + tokentime[x] + ", " + tokeny[x] + ", " + referralid + ", " + dataid + ");");
       
                connect.queryUpdate(sql);
                x++;
        }
        
        return toReturn;
      
    }
    
    
    // Use @XmlMimeType to map to DataHandler on the client side
    @WebMethod()
    @WebResult(name="result")
    public void fileUpload(@WebParam(name="name")String name, @WebParam(name="data")String data) {
      
        byte[] buf = new byte[]{0x12, 0x23};
        try {        
            // Convert base64 string to a byte array
            buf = new sun.misc.BASE64Decoder().decodeBuffer(data);
              
    
        } catch (IOException e) {
        }

    
        SqlNet connect = new SqlNet();
        
        String sql;
        
        sql = new String("INSERT INTO triage.rxdata" +
                 "(referralid, edfcontent) VALUES (?,?);");
        
        connect.queryBlob(sql, buf);
        
        return;
    }
    
}
