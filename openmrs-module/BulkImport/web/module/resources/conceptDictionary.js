function _getEl(elName) {
	return document.getElementById(elName);
}

function validateFields(fieldNames) {
	noErrors = true;
	for (var i = 0; i < fieldNames.length; i++) {
		if (_getEl(fieldNames[i]).value == "") {
			_getEl(fieldNames[i] + 'Error').style.display = "inline";
			noErrors = false;
		} else {
			_getEl(fieldNames[i] + 'Error').style.display = "none";
		}
	}
	return noErrors;
}

function validateForm(type) {
	if (type == "import"){
		noErrors = validateFields([ "csvFile", "conceptSource"]);
		if (noErrors) {
			// startConceptCounter() 
			_getEl("messageBoxBody").innerHTML = "";;
		}
		return noErrors;
	}
}

function printMessage(message) {
	document.getElementById("messageBox").style.display = "block";
	var newDiv = document.createElement("div");
	if (message.substring(0,5) == "ERROR") {
		newDiv.setAttribute("class", "error");
	}
	newDiv.innerHTML = message;
	document.getElementById("messageBoxBody").appendChild(newDiv);
}

var conceptCountInit = 0;
var conceptCounter;

function updateConceptCount(response) {
	if (conceptCountInit == 0) {
		conceptCountInit = response;
	} else {
		var conceptCount = response - conceptCountInit;
		_getEl("conceptCount").innerHTML = conceptCount;
	}
}

function getConceptCount() {
	newScript = document.createElement("script");
	newScript.setAttribute("src", "../../moduleServlet/bulkimport/conceptCounterServlet");
	newScript.setAttribute("type", "text/javascript");
	document.body.appendChild(newScript);
}

function startConceptCounter() {
	printMessage("Starting Import");
	conceptCounter = setInterval("getConceptCount()", 30000);
}

function stopConceptCounter() {
	getConceptCount();
	clearInterval(conceptCounter);
}