/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ws;

import javax.jws.*;
import java.sql.*;
import java.util.Calendar;
import java.text.*;
import java.io.*;


/**
 *
 * @author User
 */
@WebService(
            name = "CreateC",
            serviceName = "CreateCaseService",
            portName = "CreateCasePort")
public class CreateCase {
    
    private String errormsg = "";
    private String[] hasNullValue;
    private boolean newmsg = false;

    private DocUser doctor = new DocUser();
    
    public static Date getCurrentJavaSqlDate() {
        java.util.Date today = new java.util.Date();
        return new java.sql.Date(today.getTime());
    }
    
    public int hasNullValue(String userkey, String reason,  
            String institutionid, String docname, String status) 
    {
        hasNullValue = new String[5];
        int x=0;
        
        if (userkey == null) {
            hasNullValue[x] = "userkey";
            x++;
        }
        
        if (reason == null) {
            hasNullValue[x] = "reasom";
            x++;
        }
       
        if (institutionid == null) {
            hasNullValue[x] = "institutionid";
            x++;
        }
        
        if (docname == null) {
            hasNullValue[x] = "docname";
            x++;
        }
        
        if (status == null) {
            hasNullValue[x] = "status";
            x++;
        }
        
        return x;
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
    public boolean createCase(@WebParam(name="userkey") String userkey, 
            @WebParam(name="description") String description, @WebParam(name="reason") String reason,
            @WebParam(name="patientid") String patientid, 
            @WebParam(name="institutionid") String institutionid, @WebParam(name="docname") String docname,  
            @WebParam(name="docnum") String docnum)
    {
                   
 /*       if (!doctor.DocLoggedIn()) {
            this.errormsg = "ACCESS DENIED: PLEASE LOG-IN FIRST.";
            System.out.println(errormsg);
            return false;
        }
   
    String referrer = this.doctor.getUser();
  */
        
    boolean toReturn = true;
    SqlNet connect = new SqlNet();
    String status = "open";
    
        if (hasNullValue(userkey, reason, institutionid, docname, status) > 0) {
            errormsg = new String("CREATE CASE ERROR: Please Fill-Out the REQUIRED Field " + hasNullValue    + ".");
            System.err.println(errormsg);
            newmsg = true;
            return false;
        }
    
        java.util.Date timestamp = Calendar.getInstance().getTime();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
    
        String sql = new String("INSERT INTO triage.referral" +
                 "(description, reason, patientid, timestamp, institutionid, docname, docnum, status) " +
                 "VALUES ('" + description + "', '" +
                 reason + "', '" + patientid + "', '" + sdf.format(timestamp) + "', '" +
                 institutionid + "', '" + docname + "', '" +
                 docnum + "', '" + status + "');");
        
        connect.queryUpdate(sql); 
   /*
        ConnectionService conn = connect.getConnection();
        PreparedStatement pstmt = null;
        
        try {
             
    
             sql = new String("INSERT INTO triage.referral(timestamp) VALUES(?)");
    
             pstmt = conn.getConnection().prepareStatement(sql);
             Date date = getCurrentJavaSqlDate();
    
             pstmt.setDate(1, date);

             pstmt.executeUpdate();
        
             System.err.println(errormsg);
        
             pstmt.close();
             conn.getConnection().close();
        } catch(Exception ex) {}
    */
        
        return toReturn;
      
    }
    
    @WebMethod()
    @WebResult(name="result")
    public boolean upload(@WebParam(name="userkey") String userkey, @WebParam(name="fileid") String fileid, @WebParam(name="referralid") String referralid, 
            @WebParam(name="responseid") String responseid, @WebParam(name="filename") String filename,
            @WebParam(name="filetype") String filetype,@WebParam(name="filecontent") File filecontent) {
        
        boolean toReturn = true;
        SqlNet connect = new SqlNet();
        
        String sql = new String("INSERT INTO triage.file" +
                 "(fileid, referralid, responseid, filename, filetype, filecontent) VALUES (?,?,?,?,?,?);");
        
//        connect.queryBlob(sql,fileid,referralid,responseid,filename,filetype,filecontent); 
        
        return toReturn;
    }
    
   /* @WebMethod
    public static boolean upload(String source)
    {
        boolean toReturn = false;
        
        try
        {
            int fileSize=0;
            ByteArrayOutputStream buffer = null;
            
            String err = "";
            String file = "";
            String fileName = null;
            String type = "";
            String contentType = "multipart/form-data";
            String boundary = "";
            
            final int BOUNDARY_WORD_SIZE = "boundary=".length();
            
            SqlNet connect = new SqlNet();
            
            
          /*  BufferedInputStream bis = null;
            bis = new BufferedInputStream( new FileInputStream( source ) );

            
            if ( contentType == null || !contentType.startsWith("multipart/form-data") )
            {
                err = "Illegal ENCTYPE : must be multipart/form-data\n";
                err += "ENCTYPE set = " + contentType;
            }
            else
            {
                boundary = contentType.substring(contentType.indexOf("boundary=") + BOUNDARY_WORD_SIZE);
                boundary = "--" + boundary;
                try
                {
                    BufferedInputStream sis = bis;
                    byte[] b = new byte[1024];
                    int x=0;
                    int state=0;
                    String name=null,contentType2=null;

                    while ( (x=sis.read(b,0,1024)) > -1 )
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
                                  //  String userAgent = request.getHeader("User-Agent");
                                    String userSeparator="\\";  // default
                                /*    if ( userAgent.indexOf("Windows") != -1 )
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
            
            file fileInfo = new file();
            fileInfo.setFilecontent(byteArray);
            
            buffer.close();
            
            toReturn = true;
             
        }
	catch (Exception exception)
	{
            System.out.println(exception);
	}
        
        return toReturn;
    }
    */
}
