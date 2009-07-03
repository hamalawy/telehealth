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
            name = "ViewU",
            serviceName = "ViewUserService",
            portName = "ViewUserPort")
public class ViewUser {
    
    private String errormsg = "";
    
    private DocUser doctor = new DocUser();
    
    private ResultSetNet users;
    
    @WebMethod()
    @WebResult(name="result")
    public boolean viewUser() {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String docid = doctor.getId();
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.accounts WHERE docid = " + docid + ";");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        users = rs;
        
        try {
            
        if (users.getResulta().next()) {
            return true;
        } else {
            this.errormsg = "USER DOES NOT EXIST.";
        }
        
        } catch (Exception ex) {}
        
        return false;
    }
      
    
    
    @WebMethod()
    @WebResult(name="result")
    public boolean viewDoctors() {
        
         if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.accounts WHERE status = 'approved';");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        users = rs;
        
        try {
            
        if (users.getResulta().next()) {
            users.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = "NO USERS YET.";
        }
        
        } catch (Exception ex) {}
        
        return false;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean viewDoctorsAdmin() {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
         
        if (!doctor.getUser().equals("admin")) {
            this.errormsg = "ACCESS DENIED: YOU ARE NOT AUTHORIZED.";
            System.out.println(errormsg);
            return false;
        }
       
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.accounts");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        users = rs;
        
        try {
            
        if (users.getResulta().next()) {
            users.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = "NO USERS YET.";
        }
        
        } catch (Exception ex) {}
        
        return false;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean getNextDoctor() {
        
        try 
        {
            if (users.getResulta().next()) {
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
     
    @WebMethod()
    @WebResult(name="result")
    public String getItem(String item){
        
        String name = "";
        
        try {
            name = users.getResulta().getString(item);
            System.out.println(name);
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception~");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
        
           //try { users.getResulta().close(); } catch (Exception exception) { }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return name ;
    }

}
