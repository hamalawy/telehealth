/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import com.sun.xml.ws.api.*;

/**
 *
 * @author User
 */
@WebService(
            name = "ViewC",
            serviceName = "ViewCaseService",
            portName = "ViewCasePort")
public class ViewCase {

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
    
    @WebMethod()
    @WebResult(name="result")
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
    
    /* USABLE METHOD */

    @WebMethod()
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
    
    
    @WebMethod()
    @WebResult(name="result")
    public String[] viewCase(@WebParam(name="caseid") String caseid) {
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM triage.referral WHERE referralid = '" + caseid + "';");
        SqlNet user = new SqlNet();
        rs = user.query(sql);
        String[] item = new String[9];
        int x=0;
        
        cases = rs;
        
        try {
            
               cases.getResulta().next();
              
               item[0] = getCaseItem("referralid");
               item[1] = getCaseItem("description");
               item[2] = getCaseItem("reason");
               item[3] = getCaseItem("patientid");
               item[4] = getCaseItem("timestamp");
               item[5] = getCaseItem("institutionid");
               item[6] = getCaseItem("docname");
               item[7] = getCaseItem("docnum");
               item[8] = getCaseItem("status");
               System.out.println(item[1]);
               
               while (x <= 8)
               {
                   if (item[x] == null) {
                       item[x] = "";
                   }
                   
                   x++;
               }
        
        } catch (Exception ex) {}
        
        return item;
    }
    
    /* USABLE METHOD */
	
    @WebMethod()
    @WebResult(name="result")
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
    
    @WebMethod()
    @WebResult(name="result")
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
    
    @WebMethod()
    @WebResult(name="result")
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
    
    @WebMethod()
    @WebResult(name="result")
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
     
    @WebMethod()
    @WebResult(name="result")
    public String getCaseMsg() {
        
        String message = this.errormsg;
        
        this.errormsg = "";
        
        return message;
    }
    
    @WebMethod()
    @WebResult(name="result")
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
    @WebMethod()
    @WebResult(name="result")
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
    
   
    @WebMethod()
    @WebResult(name="result")
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

    @WebMethod()
    @WebResult(name="result")
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

    @WebMethod()
    @WebResult(name="result")
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
    
    
    @WebMethod()
    @WebResult(name="result")
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