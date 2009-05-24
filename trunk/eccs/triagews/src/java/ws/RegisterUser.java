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
            name = "RegisterU",
            serviceName = "RegisterUserService",
            portName = "RegisterUserPort")
public class RegisterUser {
    
    private String errormsg = "";
    private String hasNullValue;
    private boolean newmsg = false;
    
    private DocUser doctor = new DocUser();
    
    public boolean valueExists(String item, String value) {
        
        String sql = new String("SELECT * FROM telemedicine.accounts WHERE " + item + " = '" + value + "';");
        SqlNet user = new SqlNet();
        ResultSetNet rs;
        boolean valueExists = false;
        
        try {
            
            rs = user.query(sql);
        
            if (rs.getResulta().first()) {
                valueExists = true;
            }
            
            System.out.println("Value: " + valueExists);
             System.out.println("Given E-mail: " + value);
            
        } catch (Exception ex) {
            System.out.println("Got an regPAGE exceptionzzzz too?!?");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
        
        return valueExists;
    }
    
    public boolean hasNullValue(String username,String password,String firstname,String lastname,
            String middlename,String email,String hospital, String domain) 
    {
        if (username.equals("")) {
            hasNullValue = "username";
            return true;
        }
        if (password.equals("")) {
            hasNullValue = "password";
            return true;
        }
        if (firstname.equals("")) {
            hasNullValue = "firstname";
            return true;
        }
        if (lastname.equals("")) {
            hasNullValue = "lastname";
            return true;
        }
        if (middlename.equals("")) {
            hasNullValue = "middlename";
            return true;
        }
        if (email.equals("")) {
            hasNullValue = "email";
            return true;
        }
        if (hospital.equals("")) {
            hasNullValue = "hospital";
            return true;
        }
        if (domain.equals("")) {
            hasNullValue = "domain";
            return true;
        }
        
        return false;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean newRegistermsg() {
        return this.newmsg;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getRegistermsg() {
        
        String message;
        
        message = this.errormsg;
        
        this.errormsg = "";
        
        this.newmsg = false;
        
        return message;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean registerUser(@WebParam(name="username") String username,@WebParam(name="password") String password,
            @WebParam(name="firstname") String firstname,@WebParam(name="lastname") String lastname,
            @WebParam(name="middlename") String middlename,@WebParam(name="email") String email,
            @WebParam(name="hospital") String hospital, @WebParam(name="specialization") String domain)
    {
        
    boolean toReturn = true;
    SqlNet connect = new SqlNet();
    
    String status = "pending";
    
        if (hasNullValue(username,password,firstname,lastname,middlename,email,hospital,domain)) {
            errormsg = new String("REGISTRATION ERROR: Please Fill-Out ALL the Fields.");
            System.err.println(errormsg);
            newmsg = true;
            return false;
        }
    
        if (valueExists("username",username)) {
            errormsg = "REGISTRATION ERROR: Username Already Exists.";
            System.err.println(errormsg);
            newmsg = true;
            return false;
        }
    
        if (valueExists("email",email)) {
            errormsg = "REGISTRATION ERROR: That E-mail Address is already in the system.";
            System.err.println(errormsg);
            newmsg = true;
            return false;
        }
        
        this.errormsg = "THANKS FOR YOUR REGISTRATION. Your Account is still PENDING. Please wait for Approval from the System Administrator in 48 hours before you can Log In.";
        this.newmsg = true;
         
        if (doctor.DocLoggedIn()) {
            
            if (doctor.getUser().equals("admin")) {
                status = "approved";
                this.errormsg = "";
                this.newmsg = false;
            }
           
        }
        
        String sql = new String("INSERT INTO telemedicine.accounts" +
                 "(username, password, lastname, firstname, middlename, hospital, email, domain, status) " +
                 "VALUES ('" + username + "', '" + password + "', '" +
                 lastname + "', '" + firstname + "', '" + middlename + "', '" +
                 hospital + "', '" + email + "', '" + domain + "', '" + status + "');");
        
        connect.queryUpdate(sql);
        
        System.err.println(errormsg);
        
        return toReturn;
      
    }
    
}
