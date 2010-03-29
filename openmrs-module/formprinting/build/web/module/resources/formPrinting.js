function getFormContent() {
	var htmlform = document.getElementsByTagName("htmlform")[0].innerHTML;
	document.getElementById("formcontent").value = htmlform;
}

function newEl(elTag, elAttribs) {
	var el = document.createElement(elTag);
	for (o = 0; o < elAttribs.length; o++) {
		el.setAttribute(elAttribs[o][0],elAttribs[o][1]);
	}
	return el;
}

function createPrintButton() {
	var printForm = newEl("form",[
	  ["target", "_blank"],
	  ["method", "post"],
	  ["onSubmit", "getFormContent()"],
	  ["action", openmrsContextPath + "/moduleServlet/formprinting/HtmlToPdfServlet"]
	]);
	var formContentText = newEl("input",[
	  ["type", "hidden"],
	  ["value", ""],
	  ["name", "formcontent"],
	  ["id", "formcontent"]
	]);
	printForm.appendChild(formContentText);
	var printButton = newEl("input",[
	  ["type", "submit"],
	  ["value", "Print"]
    ]);
	printForm.appendChild(printButton);
	var newDiv = newEl("div", []);
	newDiv.appendChild(printForm);
	htmlForm = document.getElementsByTagName("htmlform")[0];
	htmlForm.parentNode.insertBefore(newDiv, htmlForm.nextSibling);
}

createPrintButton();