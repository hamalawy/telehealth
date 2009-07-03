/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import java.sql.*;

/**
 *
 * @author User
 */
@WebService(
            name = "CreateP",
            serviceName = "CreatePatientService",
            portName = "CreatePatientPort")
public class CreatePatient {
    
    private String errormsg = "";
    private String hasNullValue;
    private boolean newmsg = false;

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
    public boolean createPatient(@WebParam(name="userkey") String userkey, @WebParam(name="patientid") String patientid, @WebParam(name="firstname") String firstname,
            @WebParam(name="middlename") String middlename, @WebParam(name="lastname") String lastname,
            @WebParam(name="sex") String sex, @WebParam(name="birthdate") String birthdate, @WebParam(name="age") int age, 
            @WebParam(name="agevalidity") String agevalidity, @WebParam(name="location") String location)
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
    String maidenname = "";
    
        if (hasNullValue(userkey, patientid, firstname, middlename, lastname, sex, age, agevalidity, location)) {
            errormsg = new String("CREATE PATIENT ERROR: Please Fill-Out the REQUIRED Field " + hasNullValue + ".");
            System.err.println(errormsg);
            newmsg = true;
            return false;
        }
        
        String sql = new String("INSERT INTO triage.patient" +
                 "(patientid, firstname, middlename, lastname, maidenname, sex, birthdate, age, agevalidity, location) " +
                 "VALUES ('" + patientid + "', '" + firstname + "', '" +
                 middlename + "', '" + lastname + "', '" + maidenname + "', '" +
                 sex + "', '" + birthdate + "', " + age + ", '" + agevalidity + "','" + location + "');");
        
        connect.queryUpdate(sql);
    
        return toReturn;
      
    }
    
}
