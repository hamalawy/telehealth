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
            name = "ViewH",
            serviceName = "ViewHospitalService",
            portName = "ViewHospitalPort")
public class ViewHospital {
    
    private ResultSetNet hospitals = null;
    
    @WebMethod()
    @WebResult(name="result")
    public void initHospital() {
        
        ResultSetNet rs;
        String sql = new String("SELECT * FROM telemedicine.hospitals;");
        SqlNet user = new SqlNet();
        
        rs = user.query(sql);
        
        hospitals = rs;

    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean getNextHospital() {
        
        try 
        {
            System.out.println("GET NEXT HOSPITAL");
            if (hospitals.getResulta().next()) {
                System.out.println("TRUE HOSPITALS!");
                return true;
            } 
        }
        catch (Exception ex) {}
        
        return false;
    }
    
    @WebMethod()
    @WebResult(name="result")
    public String getHospitalItem(String item){
        
        String name = "";
        
        try {
                name = hospitals.getResulta().getString(item);
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