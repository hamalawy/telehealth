package org.openmrs.module.bulkimport.extension;

import java.util.HashMap;
import java.util.Map;

import org.openmrs.module.web.extension.AdministrationSectionExt;

public class AdminList extends AdministrationSectionExt {

	public String getTitle() {
        return "bulkimport.module_name";
    }
    
    public Map<String, String> getLinks() {
        
        Map<String, String> map = new HashMap<String, String>();
        
        map.put("module/bulkimport/conceptDictionary.form", "bulkimport.adminlist_concept_dictionary");
        
        return map;
    }
}
