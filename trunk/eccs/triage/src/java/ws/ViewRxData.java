/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import com.sun.xml.ws.api.*;
import java.util.*;
import java.text.*;
import java.sql.*;
import javax.swing.*;

/**
 *
 * @author User
 */
@WebService(
            name = "ViewR",
            serviceName = "ViewRxDataService",
            portName = "ViewRxDataPort")
public class ViewRxData {

    private ResultSetNet cases = null;
    private ResultSetNet data = null;
    private ResultSetNet journal = null;
    private ResultSetNet single = null;
    private Case[] referral;
    private int rowNum = 0;
    
    private String errormsg = "";
    
    private DocUser doctor = new DocUser();

    private String referralid;
    private String description;
    private String reason;
    private String patientid;
    private java.util.Date timestamp;
    private String institutionid;
    private String docname;
    private String docnum;
    private String status;
    
    public boolean dateExpired(ResultSetNet rs) {
        
        java.util.Calendar today =  new java.util.GregorianCalendar();
        String sql;
        SqlNet user = new SqlNet();
        boolean expired = false;
        SimpleMail mail = new SimpleMail();
        
        try {
        
        while (rs.getResulta().next()) {
            if (rs.getResulta().getDate("dateexpiry").before(today.getTime())) {
                
                errormsg = new String("Case #" + rs.getResulta().getString("caseid") + " with description '" + rs.getResulta().getString("shortdesc") + "' from " + rs.getResulta().getString("referrer") + 
                        " to " + rs.getResulta().getString("docname") + " has expired." );
                
                sql = new String("UPDATE telemedicine.cases SET docname = '', status = 'saved', referstatus = 'unsent', datesent = null, dateexpiry = null WHERE caseid = " + rs.getResulta().getString("caseid") + ";");              
                user.queryUpdate(sql);
                expired = true;
                
                ResultSetNet rs2, rs3;
                
                String sql2 = new String("SELECT email FROM telemedicine.accounts WHERE username = '" + rs.getResulta().getString("docname") + "';");
                String sql3 = new String("SELECT email FROM telemedicine.accounts WHERE username = '" + rs.getResulta().getString("referrer") + "';");
                
                rs2 = user.query(sql2);
                rs3 = user.query(sql3);
                
                String recipients = new String(rs2.getResulta().getString("email") + "," + rs3.getResulta().getString("email"));
                
                mail.sendMail("TELEMEDICINE PHILIPPINES: Case Referral Expired ", errormsg, "TelemedicinePhilippines", recipients);
                
            }
        }
        } catch (Exception ex) {}
        
        return expired;
    }
    
    @WebMethod
    public boolean openCase(@WebParam(name="caseid") String caseid) {
        
         if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
         
        String name = doctor.getUser();
         
        String sql = new String("UPDATE telemedicine.cases SET referstatus = 'open' WHERE docname = '" + name + "' AND caseid = " + caseid + " AND referstatus = 'new';");
        SqlNet user = new SqlNet();
        
         if (caseid.equals("")) {
            errormsg = new String("REFER ERROR: Please enter a value for 'caseid'.");
            return false;
        }
        
        user.queryUpdate(sql);
        return true;

    }
    
    public int getRowSize(ResultSetNet rs)
    {
        int rowsize = 0;
        
        try {
            
       
        while(rs.getResulta().next()) {
            rowsize++;
        }
        
        rs.getResulta().beforeFirst();
        
        } catch (Exception ex) {}
       
        return rowsize;
    }
    
/*    public java.util.Date timestamp(String time)
    {
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        java.util.Date today;
        
        try
        {
            today = df.parse(time);            
            System.out.println("Today = " + df.format(today));
        } catch (ParseException e)
        {
            e.printStackTrace();
        }
        
        return today;
    }*/

    /* USABLE METHOD */

    @WebMethod
    public String[] getCases(@WebParam(name="patientid")String patientid) {
        
    /*     if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
         
         if (!doctor.getUser().equals("admin")) {
            this.errormsg = "ACCESS DENIED: YOU ARE NOT AUTHORIZED.";
            System.out.println(errormsg);
            return false;
        }*/
         
        ResultSetNet rs;
        String sql = new String("SELECT * FROM triage.referral WHERE patientid = '" + patientid + "';");
        SqlNet user = new SqlNet();
        
        int x = 0;
        
        rs = user.query(sql);
        String[] caseid = new String[getRowSize(rs)];
        cases = rs;
        
        try {
            
          /*  rowNum = cases.getResulta().getR
        
            if (rowNum == 0) {
                this.errormsg = "YOU HAVE NO CASES.";
                System.out.println(errormsg);
                //return null;
            } else {
                System.out.println("NUMBER OF ROWS: " + rowNum);
            }
           
        */
            
            while (cases.getResulta().next()) {
              
               caseid[x] = getCaseItem("referralid");
               System.out.println(caseid[x]);
               if (caseid[x] == null) {
                    caseid[x] = "";
               }
               x++;
            }
         
        } catch (Exception ex) {}
        
        return caseid;

    }
    
    
    @WebMethod
    public String viewRxData(@WebParam(name="caseid") String caseid) {
        
        ResultSetNet rs;
        String sql= new String("SELECT heartrate FROM triage.rxdata WHERE referralid = '" + caseid + "' ORDER BY timestamp desc;");
 
        SqlNet user = new SqlNet();
        rs = user.query(sql);
        String item = new String();
        //Date time = timestamp(timestamp);
        //long inttime = time.getTime();
        
        data = rs;
        
        try {
            
               data.getResulta().next();
               
               item = getDataItem("heartrate");
        
        } catch (Exception ex) {}
        
        return item;
    }
    
  /*  @WebMethod
    public String fileDownload(@WebParam(name="name")String name, @WebParam(name="caseid")String caseid) {
      
        File someFile = new File(name);
        ResultSetNet rs = null;
        
        try {
        // Convert a byte array to base64 string
        byte[] buf = new byte[]{0x12, 0x23};
        
        // Convert base64 string to a byte array
        buf = new sun.misc.BASE64Decoder().decodeBuffer(data);
        
        
        FileOutputStream fos = new FileOutputStream(someFile);
        fos.write(buf);
        fos.flush();
        fos.close();
    
    } catch (IOException e) {
    }

    
        SqlNet connect = new SqlNet();
        String s = new String();

        String sql = new String("SELECT edfcontent from triage.rxdata WHERE referralid = " + caseid);
        
        rs = connect.query(sql);
        
        Blob blob = rs.getResulta().getBlob("edfcontent"); //get Blob obj by the photo field
        ImageIcon icon = new ImageIcon(blob.getBytes(1, (int)blob.length())); //read bytes from first byte to the end
        s = new sun.misc.BASE64Encoder().encode(blob.getBytes(1, (int)blob.length()));
        rs.getResulta().close(); //close resources 
        
        return;
    }
    
    /* USABLE METHOD */
	
    @WebMethod
    public boolean initCaseRxData() {
        
    /*     if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
         
         if (!doctor.getUser().equals("admin")) {
            this.errormsg = "ACCESS DENIED: YOU ARE NOT AUTHORIZED.";
            System.out.println(errormsg);
            return false;
        }*/
         
        ResultSetNet rs;
        String sql = new String("SELECT * FROM triage.rxdata;");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        data = rs;
        
        try {
            
        if (data.getResulta().next()) {
            data.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = "YOU HAVE NO CASES.";
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
    
    @WebMethod
    public boolean initCase() {
        
         if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
         
        String name = doctor.getUser();
         
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.cases WHERE referrer = '" + name + "' OR docname = '" + name + "';");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        if (dateExpired(rs)) {
            rs = user.query(sql);
        }
        
        cases = rs;
        
        try {
            
        if (cases.getResulta().next()) {
            cases.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = "YOU HAVE NO CASES.";
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
    
    @WebMethod
    public boolean initSpecCase(@WebParam(name="caseid") String caseid) {
        
         if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
         
        ResultSetNet rs;
        String name = doctor.getUser();
        String sql;
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.cases WHERE caseid = " + caseid + 
                    " AND (SELECT * FROM telemedicine.cases WHERE referrer = '" + name + "' OR docname = '" + name + "');");
        } else {
            sql = new String("SELECT * FROM telemedicine.cases WHERE caseid = " + caseid + ";");
        }
        
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        if (dateExpired(rs)) {
            rs = user.query(sql);
        }
        
        single = rs;
        
        try {
            
        if (single.getResulta().first()) {
            return true;
        } else {
            this.errormsg = "CASE DOES NOT EXIST.";
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
    
    @WebMethod
    public boolean initJournal(@WebParam(name="caseid") String caseid) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        ResultSetNet rs;
        String name = doctor.getUser();
        String sql;
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.journal WHERE caseid = " + caseid + 
                    " AND (SELECT * FROM telemedicine.cases WHERE referrer = '" + name + "' OR docname = '" + name + "');");
        } else {
            sql = new String("SELECT * FROM telemedicine.journal WHERE caseid = " + caseid + ";");
        }
        
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        journal = rs;
        
        try {
            
        if (journal.getResulta().next()) {
            journal.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = "YOU HAVE NO JOURNAL UPDATES.";
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
     
    @WebMethod
    public String getCaseMsg() {
        
        String message = this.errormsg;
        
        this.errormsg = "";
        
        return message;
    }
    
    @WebMethod
    public boolean initInCase(String status) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String name = doctor.getUser();
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.cases WHERE docname = '" + name + "' AND referstatus = '" + status + "';");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        if (dateExpired(rs)) {
            rs = user.query(sql);
        }
        
        cases = rs;
        
        try {
            
        if (cases.getResulta().next()) {
            cases.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = new String("YOU HAVE NO " + status.toUpperCase() + " CASES.");
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
    @WebMethod
    public boolean initPatientCase(String patientid) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String name = doctor.getUser();
        String sql;
        
        ResultSetNet rs;
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.cases WHERE patientid = " + patientid + " AND referrer = '" + name + "';");
        } else {
            sql = new String("SELECT * FROM telemedicine.cases WHERE patientid = " + patientid + ";");
        }
        
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        if (dateExpired(rs)) {
            rs = user.query(sql);
        }
        
        cases = rs;
        
        try {
            
        if (cases.getResulta().next()) {
            cases.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = new String("THIS PATIENT HAS NO CASES.");
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
    
   
    @WebMethod
    public boolean initOutCase(String status) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String name = doctor.getUser();
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.cases WHERE referrer = '" + name + "' AND status = '" + status + "';");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        if (dateExpired(rs)) {
            rs = user.query(sql);
        }
        
        cases = rs;
        
        try {
            
        if (cases.getResulta().next()) {
            cases.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = new String("YOU HAVE NO " + status.toUpperCase() + " CASES.");
        }
        
        } catch (Exception ex) {}
        
        return false;

    }
    
    /* USABLE METHOD */

    @WebMethod
    public boolean getNextCase() {
        
        try 
        {
            if (cases.getResulta().next()) {
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    /* USABLE METHOD */

    @WebMethod
    public boolean getNextData() {
        
        try 
        {
            if (data.getResulta().next()) {
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    
    @WebMethod
    public boolean getNextJournal() {
        
        try 
        {
            if (journal.getResulta().next()) {
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    /* USABLE METHOD */

    @WebMethod
    public String getCaseItem(String item){
        
        String name = "";
        
        try {
                name = cases.getResulta().getString(item);
                System.out.println(name);
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return name ;
    }
    
    @WebMethod
    public String getJournalItem(String item){
        
        String name = "";
        
        try {
                name = journal.getResulta().getString(item);
                System.out.println(name);
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return name ;
    }
    
    /* USABLE METHOD */

     @WebMethod
    public String getDataItem(String item){
        
        String name = "";
        
        try {
                name = data.getResulta().getString(item);
                System.out.println(name);
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return name ;
    }
    
    
}