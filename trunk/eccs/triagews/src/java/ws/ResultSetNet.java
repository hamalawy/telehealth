/*
 * ConnectionService.java
 * 
 * Created on Jan 10, 2008, 10:00:08 AM
 * 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import java.sql.*;
import javax.servlet.http.*;
import javax.jws.*;

/**
 *
 * @author User
 */

public class ResultSetNet {
    
    private ResultSet rs;
    
    public ResultSetNet() {}
    
    public ResultSetNet(ResultSet rs) {
        this.rs = rs;
    }
    
    public ResultSet getResulta() {
        return this.rs;
    }
    
}
