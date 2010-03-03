<%@ include file="/WEB-INF/template/include.jsp" %>
<%@ include file="/WEB-INF/template/header.jsp" %>

<style>
	#messageBox {display:none; }
	iframe {display:none; }
</style>
<script type="text/javascript" src="../../moduleResources/bulkimport/conceptDictionary.js"></script>

<h2><spring:message code="bulkimport.manageConceptDictionary"/></h2><br>
<div class="boxHeader"><spring:message code="bulkimport.importConcepts"/></div>
<div class="box">
	<form action="${pageContext.request.contextPath }/moduleServlet/bulkimport/conceptDictionaryServlet" 
		onSubmit="return validateForm('import')" enctype="multipart/form-data" method="post"
		target="uploadResult">
	<input type="hidden" name="action" value="import"/>
	<table>
		<tr>
			<td><spring:message code="bulkimport.selectConceptSource"/>: </td>
			<td>
				<select id="conceptSource" name="conceptSource">
              	<c:forEach var="source" items="${sources}">
              		<option>${source.name}</option>
				</c:forEach>
				</select>
				<span class="error" id="conceptSourceError" style="display:none">
					<spring:message code="bulkimport.conceptSourceMissing"/>
				</span>
				<a href="${pageContext.request.contextPath}/admin/concepts/conceptSource.form">Add Concept Source</a>
			</td>
		</tr>
		<tr>
			<td><spring:message code="bulkimport.selectCsvFile"/>: </td>
			<td>
				<input type="file" id="csvFile" name="csvFile" size="40"/>
				<span class="error" id="csvFileError" style="display:none">
					<spring:message code="bulkimport.csvFileMissing"/>
				</span>
			</td>
		</tr>
	</table>
	<div id="addConceptsButton" style="margin-top: 5px;margin-left:5px;">	
		<input type="submit" value="<spring:message code="bulkimport.import"/>"/>
	</div>
	</form>
</div>
<br/>
<div id="messageBox">
	<div class="boxHeader"><spring:message code="bulkimport.uploadResults"/></div>
	<div class="box">
		<div style="display:none;">Concepts added so far: <span id="conceptCount">0</span> (updated once every minute)</div>
		<div id="messageBoxBody"></div>
	</div>
</div>
<iframe name="uploadResult"></iframe>
<%@ include file="/WEB-INF/template/footer.jsp"%>