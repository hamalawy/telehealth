package org.openmrs.module.formprinting.extension;

//import org.openmrs.module.Extension;
import org.openmrs.module.web.extension.PortletExt;

/**
 * Extends org.openmrs.dictionary.index as defined in /metadata/config.xml file.
 */
public class HtmlFormEntry extends PortletExt {

	public String getPortletUrl() {
		return "module/formprinting/printButton.form";
	}

	public String getPortletParameters() {
		return "";
	}
}
