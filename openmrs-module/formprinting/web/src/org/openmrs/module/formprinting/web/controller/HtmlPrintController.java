package org.openmrs.module.formprinting.web.controller;

//import java.util.HashMap;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.validation.BindException;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.SimpleFormController;
import org.springframework.web.servlet.view.RedirectView;

public class HtmlPrintController extends SimpleFormController {

    /** Logger for this class and subclasses */
    protected final Log log = LogFactory.getLog(getClass());
    
    @Override
    @SuppressWarnings("unchecked")
    protected Map<String, Object> referenceData(HttpServletRequest request) throws Exception {
        //Map<String, Object> ret = new HashMap<String, Object>();
        return request.getParameterMap();
    }

    @Override
    protected Object formBackingObject(HttpServletRequest request) throws Exception {
        return request.getParameterMap();
    }

    @Override
    protected ModelAndView onSubmit(HttpServletRequest request,
            HttpServletResponse response, Object commandObject, BindException errors)
            throws Exception {
        return new ModelAndView(new RedirectView(getSuccessView()));
    }
    
}
