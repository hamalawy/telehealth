/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import java.sql.*;
import java.io.*;
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

 /*   @WebMethod()
  @WebResult(name="result")
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
  /*       
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
  /*          
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
  */  
    @WebMethod()
    @WebResult(name="result")
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
    
  @WebMethod()
  @WebResult(name="result")
    public String fileDownload(@WebParam(name="dataid")int dataid, @WebParam(name="caseid")String caseid) {
      
        //File someFile = new File(name);
        ResultSetNet rs = null;
        String s = null;
        
        try {
        // Convert a byte array to base64 string
        SqlNet connect = new SqlNet();

        String sql = new String("SELECT * from triage.rxdata WHERE referralid = '" + caseid + "' AND dataid = '" + dataid + "';");
        
        data = rs = connect.query(sql);
        data.getResulta().next();
        Blob blob = data.getResulta().getBlob("edfcontent"); //get Blob obj by the photo field
        s = new sun.misc.BASE64Encoder().encode(blob.getBytes(1, (int)blob.length()));
        System.out.println("dataid: " + data.getResulta().getInt("dataid"));
        
        rs.getResulta().close(); //close resources 
    } catch (Exception e) {
        System.out.println("Got a downloadex");
            System.out.println(e.getMessage());
            e.printStackTrace();
    }
        return s;
    }
   
  
  //TEMPORARY METHOD: --jerome
  @WebMethod()
  @WebResult(name="result")
    public String getLatestEDF() {
      
        //File someFile = new File(name);
        ResultSetNet rs = null;
        String s = null;
        
        try {
        // Convert a byte array to base64 string
        SqlNet connect = new SqlNet();

        String sql = new String("SELECT edfcontent from triage.rxdata ORDER BY dataid DESC LIMIT 1");
        
        data = rs = connect.query(sql);
        data.getResulta().next();
        Blob blob = data.getResulta().getBlob("edfcontent"); //get Blob obj by the photo field
        s = new sun.misc.BASE64Encoder().encode(blob.getBytes(1, (int)blob.length()));
        System.out.println("dataid: " + data.getResulta().getInt("dataid"));
        
        rs.getResulta().close(); //close resources 
    } catch (Exception e) {
        System.out.println("Got a downloadex");
            System.out.println(e.getMessage());
            e.printStackTrace();
    }
        return s;
    }  
    
   
    /* USABLE METHOD */


    @WebMethod()
    @WebResult(name="result")
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
    
    @WebMethod()
    @WebResult(name="result")
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

     @WebMethod()
     @WebResult(name="result")
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