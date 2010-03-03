package org.openmrs.module.bulkimport.web.servlet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Locale;
import java.util.HashMap;
import java.util.StringTokenizer;

import java.text.ParseException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileItemFactory;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload; 
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.openmrs.Concept;
import org.openmrs.ConceptClass;
import org.openmrs.ConceptDatatype;
import org.openmrs.ConceptMap;
import org.openmrs.ConceptName;
import org.openmrs.ConceptDescription;
import org.openmrs.ConceptSource;
import org.openmrs.api.ConceptService;
import org.openmrs.api.context.Context;
import org.openmrs.api.APIException;


/*
 * This servlet handles the parsing of CSV files for importing into the concept dictionary
 */
public class ConceptDictionaryServlet extends HttpServlet {

    private static final long serialVersionUID = 0L;
    private Log log = LogFactory.getLog(getClass());
    private PrintWriter output;

    @Override 
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        log.debug("doGet");
        output = response.getWriter();
        output.print("bulkimport:ConceptDictionary servlet");
    }
    
    /*
     * procedure for sending fail messages to the parent window;
     */
    private void fail(String message) {
    	printMessage("ERROR: " + message);
    	outputClose();
    	log.error(message);
    }
    
    /*
     * procedure for sending messages to the parent window
     */
    
    private void printMessage(String message) {
    	output.print("window.parent.printMessage(\"");
    	//output.println(message);
    	output.print(message.replace("\"", "\\\""));
    	output.println("\");");
    }
    
    /*
     * procedure for starting the output writer
     */
    private void outputStart(HttpServletResponse response) throws IOException {
    	output = response.getWriter();
        output.println("<!DOCTYPE html><html><body>");
        output.println("<script>");
    }
    
    /*
     * procedure for closing the output writer
     */
    private void outputClose() {
    	output.println("window.parent.stopConceptCounter();");
    	output.println("</script>");
    	output.println("</body></html>");
    }
    
    @SuppressWarnings("unchecked")
	@Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
    	log.debug("bulkimport:ConceptDictionary:doPost");
        try {
        	outputStart(response);
        } catch (IOException e) {
        	fail("IOException: error in opening HttpServletResponse writer"); return;
        }

        // get file items (text inputs and files) from form
        List<FileItem> fiList = null;
        try {
            FileItemFactory fiFactory = new DiskFileItemFactory();
            ServletFileUpload sfUpload = new ServletFileUpload(fiFactory);
            if (!request.getHeader("content-type").contains("application/x-www-form-urlencoded"))        
            	fiList = sfUpload.parseRequest(request);
            else 
            	fiList = new ArrayList<FileItem>();
        } catch (FileUploadException e) {
            fail("Upload error: " + e.toString()); return;
        }        
	    	
	    try {
	        HashMap<String,String> params = new HashMap<String,String>();
	        HashMap<String,FileItem> filesUploaded = new HashMap<String,FileItem>();
	                
	        // Separate inputs from files
	    	for (FileItem fileItem: fiList) {
	    		if (fileItem.isFormField()) 
	    			params.put(fileItem.getFieldName(), fileItem.getString());
	    		else 
	    			filesUploaded.put(fileItem.getFieldName(), fileItem);
	    	}
	    	
	    	// Check if a concept source has been selected, if not exist
	        if (params.get("conceptSource") == null ||params.get("conceptSource").equals("")){
	        	fail("No concept source was selected"); return;
	        }
	        // Check if action to be performed is import
	    	if (params.get("action").equals("import")){
	    		// Check if file was uploaded, if not, exist
	    		if (filesUploaded.get("csvFile") == null) {
	    			fail("No file was selected."); return;
	    		}
	        	FileItem csvFile = filesUploaded.get("csvFile"); 
	        	ConceptService conceptService = Context.getConceptService();
	
	    		// Check if concept source really exists, if not, exist
	        	ConceptSource currentSource = null;
	        	try {
	        		currentSource = conceptService.getConceptSourceByName(params.get("conceptSource"));
	        	} catch (NoSuchMethodError e){
	        		// for OpenMRS 1.5.0, where getConceptSourceByName got removed
		        	List<ConceptSource> conceptSources = Context.getConceptService().getAllConceptSources();
		    		String conceptSourceName = params.get("conceptSource");
		            for (ConceptSource conceptSource: conceptSources){
		            	if (conceptSource.getName().equals(conceptSourceName)){
		            		currentSource = conceptSource;
		            		break;
		            	}
		            }
	        	}
	            if (currentSource == null) {
	            	fail("Concept source does not exist"); return;
	            }
	        	
	            printMessage("Concept Source: " + currentSource.getName());
	            printMessage("============================================");
	            
	            InputStreamReader isReader = new InputStreamReader(csvFile.getInputStream());
		        BufferedReader csvReader = new BufferedReader(isReader);
		        try {
			        // read first line as column headers
		        	String currentLine = csvReader.readLine();
		        	
		        	// parse column headers from first line
		        	HashMap<Integer,String> colNames  = parseColumnHeaders(currentLine);
		        	printMessage("Row 1: Column Headers: " + currentLine);
		        	
		        	// go through all the lines in the file and parse currentLine for concept data and save into concept service
		        	for (int rowNum = 2; (currentLine = csvReader.readLine()) != null; rowNum++) {
		        		Concept newConcept = parseConcept(currentLine, rowNum, currentSource, colNames);
		        		try {
		        			Context.getConceptService().saveConcept(newConcept);
		        		} catch (APIException e) {
		        			fail ("Saving concept failed."); return;
		        		}
		        		printMessage("Row " + rowNum + ": Successfully saved concept: " + newConcept.getDisplayString());
			        }
		        } catch (ParseException e) {
		        	fail (e.getMessage()); return;
		        }
	    	}
	    	else {
	    		fail("Invalid action"); return;
	    	}
	
	        printMessage("============================================");
	        printMessage("Done");
	        outputClose();
    	} catch (Exception e) {
    		fail (e.getMessage()); return;
    	}
    }
    
    /*
     * parses the first row for the column headers
     * @return HashMap of the column numbers with corresponding column headers
     */
    private HashMap<Integer,String> parseColumnHeaders(String currentLine) throws ParseException {
    	HashMap<Integer,String> myHashMap = new HashMap<Integer,String>();
    	HashMap<String,Boolean> hasAttrib = new HashMap<String,Boolean>();
    	StringTokenizer sTokenizer = new StringTokenizer(currentLine,",");
    	for (int colNum = 1; sTokenizer.hasMoreTokens(); colNum++)
    	{
    		String attribName = sTokenizer.nextToken();
    		// handle csv files with quotes around the text
    		if (attribName.startsWith("\"")) {
    			while (!attribName.endsWith("\"")) {
    				attribName = attribName + sTokenizer.nextToken();
    			}
    			attribName = attribName.substring(1, attribName.length()-1);
    		}
    		attribName = attribName.toLowerCase();
    		myHashMap.put(colNum, attribName);
    		hasAttrib.put(attribName, true);
    	}
    	if (hasAttrib.get("mapping_id") != null && hasAttrib.get("class") != null && hasAttrib.get("name") != null ) {
    		return myHashMap;
    	}
    	else {
    		throw new ParseException("At least one of the required columns is/are missing (mappid_id, class, name)", 1);
    	}
    }
    
    /*
     * procedure to set the attributes of the concept just by passing strings
     */
    private void setAttrib(Concept newConcept, String attribName, String attribValue, ConceptSource currentSource) throws ParseException {
    	// set concept name
    	if (attribName.equals("name")) {
            ConceptName conceptName = new ConceptName();
            // OpenMRS convention to use upper case for concept names
            conceptName.setName(attribValue.toUpperCase());
            conceptName.setCreator(Context.getAuthenticatedUser());
            conceptName.setDateCreated(new Date());
            
            // removing the country part as OpenMRS has problems displaying country-specific names
            Locale currLocale = new Locale(Context.getLocale().getLanguage());
            conceptName.setLocale(currLocale);
            newConcept.addName(conceptName);
            // setting as preferred name, otherwise will not display properly
            newConcept.setPreferredName(currLocale, conceptName);
            return;
    	} 
    	// set concept mappid_id
    	else if (attribName.equals("mapping_id")) {
            ConceptMap conceptMap = new ConceptMap();
            conceptMap.setSource(currentSource);
            conceptMap.setSourceCode(attribValue);
            newConcept.addConceptMapping(conceptMap);
            return;
    	} 
    	// set concept class
    	else if (attribName.equals("class")) {
    		ConceptClass conceptClass = Context.getConceptService().getConceptClassByName(attribValue);
        	if (conceptClass != null) {
        		newConcept.setConceptClass(conceptClass);
        		return;
        	} else {
        		throw new ParseException("Concept class [" + conceptClass + "] does not exist.", 0);
        	}
    	}
    	// set concept description 
    	else if (attribName.equals("description")) {
    		if (!attribValue.equals("-")) {
    			ConceptDescription conceptDescription = new ConceptDescription();
        		conceptDescription.setDescription(attribValue + "(" + currentSource.getName() + ")");
        		conceptDescription.setCreator(Context.getAuthenticatedUser());
        		conceptDescription.setDateCreated(new Date());
                // removing the country part as OpenMRS has problems displaying country-specific names
                Locale currLocale = new Locale(Context.getLocale().getLanguage());
                conceptDescription.setLocale(currLocale);
                newConcept.addDescription(conceptDescription);
    		}
            return;
    	} 
    }
    
    /*
     * Parses currentLine for concept data and save into conceptService
     * 
     * Throws an exception when fields are empty.
     * @return concept created from currentLine
     */
    private Concept parseConcept(String currentLine, Integer rowNum, ConceptSource currentSource, Map<Integer,String> colNames) throws ParseException, APIException{
        // Create a new concept    	
        Concept newConcept = new Concept();
        newConcept.setCreator(Context.getAuthenticatedUser());
        newConcept.setDateCreated(new Date());

        // Set concept type to be N/A by default
    	ConceptDatatype conceptType = Context.getConceptService().getConceptDatatypeByName("N/A");
    	newConcept.setDatatype(conceptType);  
    	
    	StringTokenizer sTokenizer = new StringTokenizer(currentLine,",");
    	String attribName, attribValue;
    	//Iterate through each comma separated string of the line
        for (int colNum = 1; sTokenizer.hasMoreTokens(); colNum++) {
        	attribValue = sTokenizer.nextToken();
    		
    		// handle csv files with quotes around the text
    		if (attribValue.startsWith("\"")) {
    			while (!attribValue.endsWith("\"")) {
    				attribValue = attribValue + sTokenizer.nextToken();
    			}
    			attribValue = attribValue.substring(1, attribValue.length()-1);
    		}
    		// remove leading and trailing spaces
    		attribValue = attribValue.trim();
    		
    		// go through the columns and set the attributes into the concept
    		if (colNames.get(colNum) != null ) {
    			attribName = colNames.get(colNum); 
    			if (!attribValue.equals("")) {
    				setAttrib(newConcept, attribName, attribValue, currentSource);
    			} else {
    				throw new ParseException("Blank concept "+ attribName + " not allowed.", rowNum);
    			}
    		}
    	}
        return newConcept;
    }
}