package org.openmrs.module.formprinting.extension;

import java.util.List;
import java.util.ArrayList;
import org.openmrs.module.web.extension.HeaderIncludeExt;

public class HeaderInclude extends HeaderIncludeExt {

	public List<String> getHeaderFiles() {
		List<String> myHeaderFiles = new ArrayList<String>();
		myHeaderFiles.add("/scripts/dojoConfig.js");
		myHeaderFiles.add("/scripts/dojo/dojo.js");
		myHeaderFiles.add("/moduleResources/formprinting/loadFormPrinting.js");
		return myHeaderFiles;
	}
}
