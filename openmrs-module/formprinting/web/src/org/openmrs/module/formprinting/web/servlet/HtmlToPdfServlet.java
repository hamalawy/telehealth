package org.openmrs.module.formprinting.web.servlet;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

//import org.apache.fop.apps.MimeConstants;
//import org.apache.fop.apps.FopFactory;
//import org.apache.fop.apps.Fop;
//import org.apache.fop.servlet.ServletContextURIResolver;

//import javax.xml.transform.Result;
import javax.xml.transform.Source;
//import javax.xml.transform.Transformer;
//import javax.xml.transform.TransformerFactory;
//import javax.xml.transform.sax.SAXResult;
import javax.xml.transform.stream.StreamSource;

//import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

//import org.apache.commons.io.output.ByteArrayOutputStream;

/*
 * This servlet handles the parsing of CSV files for importing into the concept dictionary
 */
public class HtmlToPdfServlet extends HttpServlet {

    private static final long serialVersionUID = 0L;
    private Log log = LogFactory.getLog(this.getClass());
//    private ServletContextURIResolver uriResolver; 

    @Override
    public void init() throws ServletException {
    	// cannot be done because of OpenMRS servlet limitation:
    	// http://openmrs.org/wiki/Module_Servlets
    	// uriResolver = new ServletContextURIResolver(getServletContext());
    }
    
    @Override 
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        log.debug("doGet");
        PrintWriter output = response.getWriter();
        output.println("formprinting:HtmlToPdf servlet:doGet");
//        output.println("uriResolver is " + (uriResolver != null));
        File dir1 = new File (".");
        output.println(dir1.getCanonicalPath());
	    //Setup Transformer
	    
        try {
        	//Source xsltSrc = uriResolver.resolve("servlet-context:/WEB-INF/view/module/formprinting/resources/xhtml2fo-ibm.xsl", null);
        	Source xsltSrc = new StreamSource(new File("foo-xml2fo.xsl"));
        	output.print(xsltSrc != null);
        } catch (Exception e) {
        	e.printStackTrace(output);
        }
    }
    
	@Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		PrintWriter output = response.getWriter();
		response.setContentType("text/html");
		output.println("<html><head>");
		output.println("<link href='../../openmrs.css' rel='stylesheet'/>");
		output.println("<link href='../../style.css' rel='stylesheet'/>");
		output.println("<link href='../../moduleResources/htmlformentry/htmlFormEntry.css' rel='stylesheet'/>");
		output.println("<link href='../../moduleResources/formprinting/formprinting.css' rel='stylesheet'/>");
		output.println("</head><body><div id='htmlform_wrapper'>");
		try {
			output.println(request.getParameter("formcontent")); 
		} catch (NullPointerException e) {
			log.debug("parameter formcontent must contain something", e);
			throw new IOException("Parameter formcontent must contain something");
		}
		output.println("<script type='text/javascript'>window.print();</script>");
		output.println("</div>");
		output.println("</body></html>"); 
		/*
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		try {
			// sample code from http://xmlgraphics.apache.org/fop/0.95/servlets.html
			FopFactory fopFactory = FopFactory.newInstance();
			TransformerFactory tFactory = TransformerFactory.newInstance();
			fopFactory.setURIResolver(uriResolver);

		    //Setup FOP
			Fop fop = fopFactory.newFop(MimeConstants.MIME_PDF, out);
			
		    //Setup Transformer
		    //Source xsltSrc = new StreamSource(new File("foo-xml2fo.xsl"));
			Source xsltSrc = uriResolver.resolve("servlet-context:/WEB-INF/view/module/formprinting/resources/xhtml2fo-ibm.xsl", null);
		    
			Transformer transformer = tFactory.newTransformer(xsltSrc);
	
		    //Make sure the XSL transformation's result is piped through to FOP
		    Result res = new SAXResult(fop.getDefaultHandler());
	
		    //Setup input
		    //Source src = new StreamSource(new File("foo.xml"));
		    Source src = uriResolver.resolve("servlet-context:/module/formprinting/resources/sample.xml", null);
	
		    //Start the transformation and rendering process
		    transformer.transform(src, res);
		} catch (Exception e) {
			log.debug("Fop error: ", e);
			throw new IOException("Fop error: ", e);
		}
		
	    //Prepare response
	    response.setContentType("application/pdf");
	    response.setContentLength(out.size());
	    
	    //Send content to Browser
	    response.getOutputStream().write(out.toByteArray());
	    response.getOutputStream().flush();
	    */
    }
    
}