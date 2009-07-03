/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;

/**
 *
 * @author User
 */
@WebService(
            name = "ViewP",
            serviceName = "ViewPatientService",
            portName = "ViewPatientPort")
public class ViewPatient {
    
    private ResultSetNet nameSet = null;
    private ResultSetNet history = null;
    private ResultSetNet patient = null;
    
    private String errormsg = "";
    
    private DocUser doctor = new DocUser();
    
    
    /* USABLE METHOD */

    @WebMethod()
    @WebResult(name="result")
    public boolean initPatientAdmin() {
        
  /*      if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        if (!doctor.getUser().equals("admin")) {
            this.errormsg = "ACCESS DENIED: YOU ARE NOT AUTHORIZED.";
            System.out.println(errormsg);
            return false;
        }
    */    
        ResultSetNet rs;
        String sql = new String("SELECT * FROM triage.patient;");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        nameSet = rs;
        
        try {
            
        if (nameSet.getResulta().next()) {
            nameSet.getResulta().beforeFirst();
            return true;
        } else {
            this.errormsg = "YOU HAVE NO PATIENTS.";
        }
        
        } catch (Exception ex) {}
        
        return false;
        
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
    @WebMethod()
    @WebResult(name="result")
    public String[] searchPatients(@WebParam(name="lastname")String lastname, @WebParam(name="firstname")String firstname) {
        
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
        String sql = new String("SELECT * FROM triage.patient WHERE lastname = '" + lastname + 
                                "' AND firstname = '" + firstname + "';");
        SqlNet user = new SqlNet();
        
        int x = 0;
        
        rs = user.query(sql);
        String[] patients = new String[getRowSize(rs)];
        
        nameSet = rs;
        
        try {
            
          /*  rowNum = Patients.getResulta().getR
        
            if (rowNum == 0) {
                this.errormsg = "YOU HAVE NO PatientS.";
                System.out.println(errormsg);
                //return null;
            } else {
                System.out.println("NUMBER OF ROWS: " + rowNum);
            }
           
        */
            
            while (nameSet.getResulta().next()) {
              
               patients[x] = getPatientItem("patientid");
               System.out.println(patients[x]);
               if (patients[x] == null) {
                       patients[x] = "";
                   }
               x++;
            }
         
        } catch (Exception ex) {}
        
        return patients;
        
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String[] viewPatient(@WebParam(name="patientid") String patientid) {
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM triage.patient WHERE patientid = '" + patientid + "';");
        SqlNet user = new SqlNet();
        rs = user.query(sql);
        String[] item = new String[10];
        int x = 0;
        
        nameSet = rs;
        
        try {
            
               nameSet.getResulta().next();
              
               item[0] = getPatientItem("patientid");
               item[1] = getPatientItem("firstname");
               item[2] = getPatientItem("middlename");
               item[3] = getPatientItem("lastname");
               item[4] = getPatientItem("maidenname");
               item[5] = getPatientItem("sex");
               item[6] = getPatientItem("birthdate");
               item[7] = getPatientItem("age");
               item[8] = getPatientItem("agevalidity");
               item[9] = getPatientItem("location");
               System.out.println(item[1]);
        
               while (x <= 9)
               {
                   if (item[x] == null) {
                       item[x] = "";
                   }
                   
                   x++;
               }
        } catch (Exception ex) {}
        
        return item;
    }

    //TEMPORARY METHOD: --jerome
    @WebMethod()
    @WebResult(name="result")
    public String[] getLatestPatient() {
        
        ResultSetNet rs;
        String sql = new String("SELECT patientid FROM triage.patient;");
        SqlNet user = new SqlNet();
        rs = user.query(sql);
        nameSet = rs;
        
        try {
            nameSet.getResulta().last();
        } catch (Exception ex) {}
        
        return viewPatient(getPatientItem("patientid"));
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getPatientMsg() {
        
        String message = this.errormsg;
        
        this.errormsg = "";
        
        return message;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean initSpecPatient(String patientid) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String docid = doctor.getId();
        String sql;
        
        ResultSetNet rs;
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.patients WHERE patientid = " + patientid + " AND docid = " + docid + ";");
        } else {
            sql = new String("SELECT * FROM telemedicine.patients WHERE patientid = " + patientid + ";");
        }
        
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        patient = rs;
        
        try 
        {
           if (patient.getResulta().next()) {
            return true;
            } else {
            this.errormsg = "PATIENT DOES NOT EXIST.";
            }
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean initHistory(String patientid) {
        
        if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
        
        String sql;
        String docname = doctor.getUser();
        
        ResultSetNet rs;
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.history WHERE patientid = " + patientid + 
                    " AND (SELECT * FROM telemedicine.Patients WHERE docname = '" + docname + "' OR referrer = '" + docname + "');");
        } else {
            sql = new String("SELECT * FROM telemedicine.history WHERE patientid = " + patientid + ";");
        }
        
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        history = rs;
        
        try 
        {
            if (history.getResulta().next()) {
                return true;
            } else {
                this.errormsg = "PATIENT HISTORY DOES NOT EXIST.";
            }
        }
        catch (Exception ex) {}
        
        return false;
        
    }
            
    /* USABLE METHOD */

    @WebMethod()
    @WebResult(name="result")
    public boolean getNextPatient() {
        
        try 
        {
            if (nameSet.getResulta().next()) {
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    /* USABLE METHOD */

    @WebMethod()
    @WebResult(name="result")
    public String getPatientItem(String item){
        
        String name = "";
        
        try {
                name = nameSet.getResulta().getString(item);
                System.out.println(name);
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception~");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
        
            //try { nameSet.getResulta().close(); } catch (Exception exception) { }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return name ;
    }

    @WebMethod()
    @WebResult(name="result")
    public String getSpecPatientItem(String item){
        
        String name = "";
        
        try {
                    name = patient.getResulta().getString(item);
                    System.out.println(name);
                
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception~");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
        
            //try { nameSet.getResulta().close(); } catch (Exception exception) { }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return name ;
    }

    @WebMethod()
    @WebResult(name="result")
    public String getHistoryEntry(String field){
        
        String entry = "";
        
        try {
                
                    entry = history.getResulta().getString(field);
                    System.out.println(entry);
                
        }
        catch (Exception ex)
        {
            System.out.println("Got an exception~");
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
        
            //try { nameSet.getResulta().close(); } catch (Exception exception) { }
           // try { stmt.close(); } catch (Exception exception) { }
           // try { connection.getConnection().close(); } catch (Exception exception) { }
        return entry ;
   }
}
