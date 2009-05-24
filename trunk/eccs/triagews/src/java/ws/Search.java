/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.WebService;
import javax.jws.*;

/**
 *
 * @author User
 */
@WebService(
    name = "SearchU",
    serviceName = "SearchService",
    portName = "SearchPort")
public class Search {

    private ResultSetNet results;
    private String searchmsg = "";
    
    private DocUser doctor = new DocUser();
    
    public ResultSetNet searchPatient(String name, String key) {
        
        ResultSetNet rs;
        String sql;
        String id = doctor.getId();
                
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.patients WHERE " + name
                + " LIKE '%" + key + "%' AND docid = " + id + ";");
        } else {
            sql = new String("SELECT * FROM telemedicine.patients WHERE " + name
                + " LIKE '%" + key + "%';");
        }
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        return rs;
    }
    
    public ResultSetNet searchCase(String desc, String key) {
        
        ResultSetNet rs;
       
        String sql = new String("SELECT * FROM telemedicine.cases WHERE " + desc
                + " LIKE '%" + key + "%';");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        return rs;    
    }
    
    public ResultSetNet searchPatientCombo(String name1, String name2, String rel, String key) {
        
        ResultSetNet rs;
        String sql;
        String id = doctor.getId();
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.patients WHERE " + name1
                + " LIKE '%" + key + "%' " + rel.toUpperCase() + " " + name2 + " LIKE '%" + key
                + "%' AND (SELECT * FROM telemedicine.patients WHERE docid = " + id + ");");
        } else {
            sql = new String("SELECT * FROM telemedicine.patients WHERE " + name1
                + " LIKE '%" + key + "%' " + rel.toUpperCase() + " " + name2 + " LIKE '%" + key
                + "%';");
        }
        
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        return rs;
    }
    
    public ResultSetNet searchCaseCombo(String desc1, String desc2, String rel, String key) {
        
        ResultSetNet rs;
       
        String sql = new String("SELECT * FROM telemedicine.cases WHERE " + desc1
                + " LIKE '%" + key + "%' " + rel.toUpperCase() + " " + desc2 + " LIKE '%" + key
                + "%';");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        return rs;    
    }
    
    public ResultSetNet searchCaseid(String key) {
        
        ResultSetNet rs;
       
        String sql = new String("SELECT * FROM telemedicine.patients WHERE caseid = " + key + ";");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        return rs;    
    }
    
    public ResultSetNet searchPatientid(String key) {
        
        ResultSetNet rs;
        String sql;
        String id = doctor.getId();
        
        if (!doctor.getUser().equals("admin")) {
            sql = new String("SELECT * FROM telemedicine.patients WHERE patientid = " + key + " AND docid = " + id + ";");
        } else {
            sql = new String("SELECT * FROM telemedicine.patients WHERE patientid = " + key + ";");
        }
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        return rs;
    }
   
    
    @WebMethod()
    @WebResult(name="result")
    public boolean initSearch(String table, String item, String key) {
        
        if (!doctor.DocLoggedIn()) {
            this.searchmsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(searchmsg);
            return false;
        }
        
        if (table.equals("cases")) {
            results = searchCase(item, key);
        } else {
            results = searchPatient(item, key);  
        }
        try {
            if (results.getResulta().first()) {
                results.getResulta().beforeFirst();
                return true;
            } else {
                this.searchmsg = "SEARCH: NO MATCH FOUND";
                System.out.println(this.searchmsg);
            }
        }
        catch (Exception ex) {}
        
        return false;
        
    }
    
    
    @WebMethod()
    @WebResult(name="result")
    public boolean initSearchCombo(String table, String item1, String item2, String rel, String key) {
        
         if (!doctor.DocLoggedIn()) {
            this.searchmsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(searchmsg);
            return false;
        }
         
        if (table.equals("cases")) {
            results = searchCaseCombo(item1, item2, rel, key);
        } else {
            results = searchPatientCombo(item1, item2, rel, key);  
        }
        try {
            if (results.getResulta().first()) {
                results.getResulta().beforeFirst();
                return true;
            } else {
                this.searchmsg = "SEARCH: NO MATCH FOUND";
                System.out.println(this.searchmsg);
            }
        }
        catch (Exception ex) {}
        
        return false;
        
    }
    
    public boolean initSearchid(String table, String id) {
        
         if (!doctor.DocLoggedIn()) {
            this.searchmsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(searchmsg);
            return false;
        }
         
        if (table.equals("cases")) {
            results = searchCaseid(id);
        } else {
            results = searchPatientid(id);  
        }
        try {
            if (results.getResulta().first()) {
                results.getResulta().beforeFirst();
                return true;
            } else {
                this.searchmsg = "SEARCH: NO MATCH FOUND";
                System.out.println(this.searchmsg);
            }
        }
        catch (Exception ex) {}
        
        return false;
        
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getSearchMsg() {
        
        String message = this.searchmsg;
        
        this.searchmsg = "";
        
        return message;
    }
            
    @WebMethod()
    @WebResult(name="result")
    public boolean getNextSearch() {
        
        try 
        {
            if (results.getResulta().next()) {
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getSearchItem(String table, String item) {
        
        String value = "";
        
        try 
        {
            
        if (table.equals("cases")) {
            if (item.equals("shortdesc") || item.equals("referrer") || item.equals("caseid")) {
                value = results.getResulta().getString(item);
                return value;
            }
            else {
                searchmsg = "SEARCH ITEMS ARE LIMITED TO 'shortdesc', 'referrer' and 'caseid'.";
                return value;
            }
        }
            value = results.getResulta().getString(item);
        }
        catch (Exception ex) {}
        
        return value;
          
    }
    
    @WebMethod()
    @WebResult(name="result")
    public void closeSearch() {
        
        try {
            results.getResulta().close();
        }
        catch (Exception ex) {}
    }
        
}
