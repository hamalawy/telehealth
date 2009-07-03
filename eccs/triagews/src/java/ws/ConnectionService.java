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
import java.util.*;
import javax.servlet.http.*;

/**
 *
 * @author User
 */
public class ConnectionService {
    private Connection connection;
    
    public ConnectionService() {}
    
    public ConnectionService(Connection connection) {
        this.connection = connection;
    }
    
    public Connection getConnection() {
        return this.connection;
    }
    

}
