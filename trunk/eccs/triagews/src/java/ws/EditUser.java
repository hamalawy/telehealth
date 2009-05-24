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
            name = "EditU",
            serviceName = "EditUserService",
            portName = "EditUserPort")
public class EditUser {
    
    private String username;
    private String errormsg = "";
    
    private DocUser doctor = new DocUser();
    
    public boolean valueExists(String item, String value) {
        
        String sql = new String("SELECT * FROM telemedicine.accounts WHERE " + item + " = '" + value + "' AND username = '"
                + username + "';");
        SqlNet user = new SqlNet();
        ResultSetNet rs;
        boolean valueExists = false;
        
        try {
            
            rs = user.query(sql);
        
            if (rs.getResulta().first()) {
                valueExists = true;
            }
            
            System.out.println("Value: " + valueExists);
            
        } catch (Exception ex) {
            System.out.println("Got an regPAGE exceptionzzzz too?!?");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
        
        return valueExists;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getEditmsg() {
        
        String message;
        
        message = this.errormsg;
        
        this.errormsg = "";
        
        return message;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean editUser(@WebParam(name="item")String item, @WebParam(name="value")String value) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String docid = doctor.getId();
        
        String sql = new String("UPDATE telemedicine.accounts SET " + item + " = '" + value + "' WHERE docid = '" + docid + "';");
        SqlNet user = new SqlNet();
        
        if (value.equals("")) {
            errormsg = new String("UPDATE ERROR: Please enter a value for '" + item + "'.");
            return false;
        }
     /*   if ((item.equals("email")) && (valueExists("email",value))) {
            errormsg = "UPDATE ERROR: That E-mail Address is already in the system.";
            return false;
        }*/
        
        System.err.println(errormsg);
        
        user.queryUpdate(sql);
        doctor.reset();
        
        return true;
      
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean changePassword(String oldpassword, String newpassword) {
        
        if (oldpassword.equals("") || newpassword.equals("")) return true;
        
        if (valueExists("password",oldpassword)) {
            editUser("password",newpassword);
            return true;
        }
        else {errormsg = "UPDATE ERROR: Incorrect Password.";}
        
        System.err.println(errormsg);
        
        return false;
    }

}
