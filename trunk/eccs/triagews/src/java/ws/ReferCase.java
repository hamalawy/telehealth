/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import com.sun.xml.ws.api.*;
import java.sql.*;
import java.util.Calendar;
import java.util.GregorianCalendar;

/**
 *
 * @author User
 */
@WebService(
            name = "ReferC",
            serviceName = "ReferCaseService",
            portName = "ReferCasePort")
public class ReferCase {
    
    private String errormsg = "";
    
    private DocUser doctor = new DocUser();
    
    public static Date getCurrentJavaSqlDate() {
        java.util.Date today = new java.util.Date();
        return new java.sql.Date(today.getTime());
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getRefermsg() {
        
        String message;
        
        message = this.errormsg;
        
        this.errormsg = "";
        
        return message;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean referCase(@WebParam(name="caseid")String caseid,@WebParam(name="docname")String docname,@WebParam(name="hours")int hours) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String name = doctor.getUser();
       
        Date date = getCurrentJavaSqlDate();
       
        
        Calendar exp = new GregorianCalendar();
        exp.add(Calendar.DATE, hours);
        java.sql.Date expiry = new java.sql.Date(exp.getTime().getTime());
         
        String sql = new String("UPDATE telemedicine.cases SET docname = '" + docname + "' WHERE caseid = " + caseid + " AND referrer = '" + name + "';");
        String sql2 = new String("UPDATE telemedicine.cases SET status = 'sent', referstatus = 'new' WHERE caseid = " + caseid + " AND referrer = '" + name + "';");
        String sql3 = new String("UPDATE telemedicine.cases SET datesent = " + date + ", dateexpiry = " + expiry + " WHERE caseid = " + caseid + " AND referrer = '" + name + "';");
        SqlNet user = new SqlNet();
        
        if (caseid.equals("")) {
            errormsg = new String("REFER ERROR: Please enter a value for 'caseid'.");
            System.out.println(errormsg);
            return false;
        }
        
        if (docname.equals("")) {
            errormsg = new String("REFER ERROR: Please enter a value for 'docname'.");
            System.out.println(errormsg);
            return false;
        }
        
        if (docname.equals(name)) {
            errormsg = new String("REFER ERROR: You can't refer a case to yourself.");
            System.out.println(errormsg);
            return false;
        }
        
     /*   if ((item.equals("email")) && (valueExists("email",value))) {
            errormsg = "UPDATE ERROR: That E-mail Address is already in the system.";
            return false;
        }*/
        
        System.err.println(errormsg);
        
        user.queryUpdate(sql);
        user.queryUpdate(sql2);
        user.queryUpdate(sql3);
        
        errormsg = new String("CASE #" + caseid + " was successfully REFERRED to " + docname + " from " + name + ".");
        System.out.println(errormsg);
        
        ResultSetNet rs2, rs3;
        SimpleMail mail = new SimpleMail();
                
        sql2 = new String("SELECT email FROM telemedicine.accounts WHERE username = '" + docname + "';");
        sql3 = new String("SELECT email FROM telemedicine.accounts WHERE username = '" + name + "';");
                
        rs2 = user.query(sql2);
        rs3 = user.query(sql3);
                
        try {
            
            String recipients = new String(rs2.getResulta().getString("email") + "," + rs3.getResulta().getString("email"));
                
            mail.sendMail("TELEMEDICINE PHILIPPINES: New Case Referral", errormsg, "TelemedicinePhilippines", recipients);
     
        } catch (Exception ex) {}
        
        return true;
      
    }
    
}
