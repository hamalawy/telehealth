package org.openmrs.module.bulkimport.web.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.openmrs.api.ConceptService;
import org.openmrs.api.context.Context;
/*
 * This servlet handles the parsing of CSV files for importing into 
 */
public class ConceptCounterServlet extends HttpServlet {

    private static final long serialVersionUID = 1L;
    private Log log = LogFactory.getLog(this.getClass());
    private PrintWriter output;

    @Override 
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        log.debug("bulkimport:ConceptCounter:doGet");
        output = response.getWriter();
    	ConceptService conceptService = Context.getConceptService();
    	output.print("updateConceptCount(" + conceptService.getAllConcepts().size() + ");");
    }
    
	@Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		log.debug("bulkimport:ConceptCounter:doPost");
    	output = response.getWriter();
    	ConceptService conceptService = Context.getConceptService();
    	output.print(conceptService.getAllConcepts().size());
    }
}