/*
 * SqlAdapter.java
 *
 * Created on January 28, 2007, 2:58 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package ws;


import java.io.*;
import java.sql.*;
import javax.jws.*;

/**
 *
 * @author Pepz Caballes
 */

public class SqlNet
{   
   
   private String errormsg = "";
   
    public ConnectionService getConnection()
    {
        ConnectionService connection = null;
         
       try
        {
            
            Class.forName("org.gjt.mm.mysql.Driver").newInstance();
    
            connection = new ConnectionService(DriverManager.getConnection("jdbc:mysql://localhost/triage?user=triageuser&password=cuv4xtriage"));
        }
        
        catch (Exception exception)
        {
            System.out.println("Got a Connection exception! "); 
            System.out.println(exception.getMessage());
            exception.printStackTrace();
        }
        return connection;
    }

    public ResultSetNet query(String sql)
    {
        ConnectionService connection = null;
        Statement stmt = null;
        ResultSetNet rs = null;
        
        try
        {
            System.out.println(sql);
            connection = getConnection();
            System.out.println("Connected!");
            stmt = connection.getConnection().createStatement();
            System.out.println("Stated!");
            rs  = new ResultSetNet(stmt.executeQuery(sql));
           
        }
        catch (Exception exception)
        {
            System.out.println("Got a Query exception!");
            System.out.println(exception.getMessage());
            exception.printStackTrace();
        }
      
        return rs;
    }
  
    public int queryUpdate(String sql)
    {
        ConnectionService connection = null;
        Statement stmt = null;
        int update = -2;
      try
        {
            System.out.println(sql);
            connection = getConnection();
            System.out.println("Connected!");
            stmt = connection.getConnection().createStatement();
            System.out.println("Created!");
            update = stmt.executeUpdate(sql);
            System.out.println("Executed!");
        }
        catch (Exception exception) {
            System.out.println("OH NOES!");
            System.out.println(exception.getMessage());
            exception.printStackTrace();
        }
        finally
        {
            try { stmt.close(); } catch (Exception exception) { }
            try { connection.getConnection().close(); } catch (Exception exception) { }
        }
        return update;
    }
  
    public int queryArray(String sql, String referralid, String ecgtime,
            String ecgy, double bloodox, double bpressure, double heartrate)
    {
    /*    ByteArrayOutputStream os = new ByteArrayOutputStream();
        ObjectOutputStream out = new ObjectOutputStream( os );
        out.String sql, String referralid, String timestamp, long[] ecgtime,
            double[] ecgy, double bloodox, double bpressure, double heartratewriteObject( ecgtime );
 
        byte[] blob = os.toByteArray();
        
        FileInputStream filec; */
        ConnectionService connection = null;
        PreparedStatement pstmt = null;
        int update = -2;
        
        try
        {
            System.out.println(sql);
            connection = getConnection();
            System.out.println("Connected!");
            connection.getConnection().setAutoCommit(false);
        
            pstmt = connection.getConnection().prepareStatement(sql);
            pstmt.setString(1, referralid);
            pstmt.setString(2, ecgtime);
            pstmt.setString(3, ecgy);
            pstmt.setDouble(4, bloodox);
            pstmt.setDouble(5, bpressure);
            pstmt.setDouble(6, heartrate);
            System.out.println("Created!");
            update = pstmt.executeUpdate();
            System.out.println("Executed!");
            connection.getConnection().commit();
        }
        catch (Exception exception) {
            System.out.println("OH NOES!");
            System.out.println(exception.getMessage());
            exception.printStackTrace();
        }
        finally
        {
            try { pstmt.close(); } catch (Exception exception) { }
            try { connection.getConnection().close(); } catch (Exception exception) { }
        }
        return update;

    }
     public int queryBlob(String sql, byte[] edfcontent) 
    {
       
        ConnectionService connection = null;
        PreparedStatement pstmt = null;
        String yes = "yeah";
        int update = -2;
        
      try
        {
            System.out.println(sql);
            connection = getConnection();
            System.out.println("Connected!");
            //connection.getConnection().setAutoCommit(false);
            pstmt = connection.getConnection().prepareStatement(sql);
            System.out.println("Prepared!");
/*            FileInputStream fis = new FileInputStream(edfcontent); //get inputStream of this file
            //pstmt.setInt(1,yes);
*/            
            pstmt.setString(1,yes); 
            pstmt.setObject(2, edfcontent, java.sql.Types.BLOB); //set parameter of blob type
            pstmt.execute(); //execute update statment
            System.out.println("Executed!");
            pstmt.close(); //close resources
            //fis.close();
   
        }
        catch (Exception exception) {
            System.out.println("OH NOES! " + update);
            System.out.println(exception.getMessage());
            exception.printStackTrace();
        }
        finally
        {
            System.out.println("UPDATE: " + update);
            try { connection.getConnection().close(); } catch (Exception exception) { }
        }
        return update;
    }
    
         
/*    public boolean queryBoolean(@WebParam(name="sql") String sql)
    {
        ConnectionService connection = null
        Statement stmt = null;
        boolean exists = false;
   
      try
        {
            connection = getConnection();
            stmt = connection.getConnection().createStatement();
            exists = stmt.execute(sql);
        }
        catch (Exception exception) { 
            
            System.out.println("Got an login exceptionzzzz too?!?");
            System.out.println(exception.getMessage());
            exception.printStackTrace();
            
        }
        finally
        {
            try { stmt.close(); } catch (Exception exception) { }
            try { connection.getConnection().close(); } catch (Exception exception) { }
        }
        return exists;
    } */
    
    public boolean passwordCheck(@WebParam(name="username") String username, @WebParam(name="password") String password) {
        
        String sql = "SELECT * FROM telemedicine.accounts WHERE username='" + username + "' AND password='" + password + "';";
        ResultSetNet rs = null;
        boolean toReturn = false;
        
        try
        {
            rs  = query(sql);
            
            if (rs.getResulta().first())
            {
                toReturn = true;
                errormsg = "";
            }
            else {
                errormsg = "LOGIN ERROR: Invalid Username and/or Password!";
                System.out.println(errormsg);
            }
        }
        catch (Exception exception) {
            
            System.out.println("Got a passwordcheck exception!");
            System.out.println(exception.getMessage());
            exception.printStackTrace();
        
        }
        finally
        {
            try { rs.getResulta().close(); } catch (Exception exception) { }
        }
        
        return toReturn;
        
    }
        
/*    @WebMethod 
    public boolean login(@WebParam(name="username") String username, @WebParam(name="password") String password)
    {
        
        boolean toReturn = false;
        
        toReturn = passwordCheck(username, password);
        
        return toReturn;
    }*/
}
    
 /* public static void createCase2(HttpServletRequest request, HttpSession session) throws java.sql.SQLException
    {
        String shortdesc = request.getParameter("shortdesc");
        String referrer = request.getParameter("referrer");
        String casedesc = request.getParameter("casedesc");
        String docname = request.getParameter("consultant");
        String status = "sent";
        
        Connection connection = null;
        Statement stmt = null;
        PreparedStatement pstmt = null;
        
        try
        {
            connection = getConnection();
            stmt = connection.createStatement();
            long date = new java.util.Date().getTime();
            java.sql.Date dateToday = new java.sql.Date(date);
            stmt.executeUpdate("INSERT INTO telemedicine.cases " +
                    "(shortdesc, datestart, datelastupdate, updates, referrer, datelastview, status, docname, casedesc) " +
                    "VALUES('" + shortdesc + "', ?, ?, ?, '" + referrer + "', ?, '" + status + 
                    "', '" + docname + "', '" + casedesc + "');" );
        }
        catch (Exception exception) { }
        finally
        {
            try { stmt.close(); } catch (Exception exception) { }
            try { connection.close(); } catch (Exception exception) { }
        }
    }
    */
 /* public static boolean createCase(HttpServletRequest request, HttpSession session) throws java.sql.SQLException
    {
        String shortdesc = request.getParameter("shortdesc");
        String referrer = request.getParameter("referrer");
        String casedesc = request.getParameter("casedesc");
        String docname = request.getParameter("consultant");
        String status = "sent";
        
        boolean toReturn = false;
        Connection connection = null;
        Statement stmt = null;
        PreparedStatement pstmt = null;*/
        
 /*       int fileid=0;
        int y;
        for(y=1;y<6;y++) { 
            if (request.getParameter("purpose" + y) == null) ;
            else
                purpose = purpose + " " + request.getParameter("purpose" + y);
        }
        try
	{
           int fileSize=0;
            ByteArrayOutputStream buffer = null;
            
            String err = "";
            String file = "";
            String fileName = null;
            String type = "";
            String contentType = request.getContentType();
            String boundary = "";
            
            final int BOUNDARY_WORD_SIZE = "boundary=".length();
            
            if ( contentType == null || !contentType.startsWith("multipart/form-data") )
            {
                err = "Ilegal ENCTYPE : must be multipart/form-data\n";
                err += "ENCTYPE set = " + contentType;
            }
            else
            {
                boundary = contentType.substring(contentType.indexOf("boundary=") + BOUNDARY_WORD_SIZE);
                boundary = "--" + boundary;
                try
                {
                    javax.servlet.ServletInputStream sis = request.getInputStream();
                    byte[] b = new byte[1024];
                    int x=0;
                    int state=0;
                    String name=null,contentType2=null;

                    while ( (x=sis.readLine(b,0,1024)) > -1 )
                    {
                        String s = new String(b,0,x);
                        if ( s.startsWith(boundary) )
                        {
                            state = 0;
                            name = null;
                            contentType2 = null;
                            fileName = null;
                        }
                        else if( s.startsWith("Content-Disposition") && state==0 )
                        {
                            state = 1;
                            if( s.indexOf("filename=") == -1 )
                                name = s.substring(s.indexOf("name=") + "name=".length(),s.length()-2);
                            else
                            {
                                name = s.substring(s.indexOf("name=") + "name=".length(),s.lastIndexOf(";"));
                                fileName = s.substring(s.indexOf("filename=") + "filename=".length(),s.length()-2);
                                if( fileName.equals("\"\"") )
                                {
                                    fileName = null;
                                }
                                else
                                {
                                    String userAgent = request.getHeader("User-Agent");
                                    String userSeparator="/";  // default
                                    if ( userAgent.indexOf("Windows") != -1 )
                                        userSeparator="\\";
                                    if ( userAgent.indexOf("Linux") != -1 )
                                        userSeparator="/";
                                    fileName = fileName.substring(fileName.lastIndexOf(userSeparator)+1,fileName.length()-1);
                                    if( fileName.startsWith("\"") )
                                        fileName = fileName.substring(1);
                                }
                                file = fileName;
                            }
                            name = name.substring(1,name.length()-1);
                            if ( name.equals("file") )
                            {
                                if ( buffer!=null )
                                    buffer.close();
                                buffer = new ByteArrayOutputStream();
                            }
                        }
                        else if( s.startsWith("Content-Type") && state==1 ) 
                        {
                            state = 2;
                            contentType2 = s.substring(s.indexOf(":")+2,s.length()-2);
                            type = contentType2;
                        }
                        else if( s.equals("\r\n") && state != 3 )
                        {
                            state = 3;
                        }
                        else
                        {
                            if ( name.equals("file") )
                            {
                                buffer.write(b,0,x);
                                fileSize+=x;
                            }
                        }
                    }
                    sis.close();
                }
                catch( java.io.IOException e )
                {
                    err = e.toString();
                }
            }
           
            byte[] byteArray = buffer.toByteArray();
            
            InputStream inputStream = new ByteArrayInputStream(byteArray);
            
            inputStream.close();
            buffer.close();
             
            long date = new java.util.Date().getTime();
            java.sql.Date dateToday = new java.sql.Date(date);
            connection = getConnection();
          stmt = connection.createStatement();) 
            pstmt = connection.prepareStatement("INSERT INTO telemedicine.cases " +
                    "(shortdesc, datestart, datelastupdate, updates, referrer, datelastview, status, docname, casedesc) " +
                    "VALUES(?,?,?,?,?,?,?,?,?);" );
            pstmt.setString( 1, shortdesc );
            pstmt.setDate( 2, dateToday );
            pstmt.setDate( 3, dateToday );
            pstmt.setInt(4, 0);
            pstmt.setString( 5, referrer );
            pstmt.setDate( 6, dateToday );
            pstmt.setString( 7, "sent" );
            stmt = connection.createStatement();
          rs = stmt.executeQuery("SELECT * FROM telemedicine.accounts WHERE username = '" + docname + "';");
            if ( rs.next() )
            {
                pstmt.setInt( 6, rs.getInt("userid") );
            } 
            pstmt.setString( 8, docname );
            pstmt.setString( 9, casedesc );
           
            pstmt.executeUpdate();
            
           inputStream.close();
            buffer.close();
            
            toReturn = true;
	}
	catch (Exception exception)
	{
            exception.printStackTrace();
	}
        
        return toReturn;
  }*/
 
