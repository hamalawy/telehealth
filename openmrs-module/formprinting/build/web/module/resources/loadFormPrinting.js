dojo.addOnLoad(function() {
	if (document.getElementsByTagName("htmlform").length>0 ) {
		var newScript = document.createElement("script");
		newScript.setAttribute("src", openmrsContextPath + "/moduleResources/formprinting/formPrinting.js");
		document.body.appendChild(newScript);
	}
});