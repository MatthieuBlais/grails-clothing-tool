<g:if test="${error}">
    <div class="alert alert-danger" role="alert">
      <strong>${error}</strong>
    </div>
</g:if>
<g:if test="${headers.size()==0 && !error}">
	<p>No result!</p>
</g:if>
<g:if test="${headers.size()>0}">
<table id="sql-table" class="display table table-striped table-bordered" style="width:100%">
    <thead>
        <tr>
            <g:each var="header" in="${headers}">
            	<th>${header}</th>
            </g:each>
        </tr>
    </thead>
    <tbody>
	    <g:each var="row" in="${rows}">
	        <tr>
	            <g:each var="item" in="${row}">
	            	<td>${item}</td>
	            </g:each>
	        </tr>
        </g:each>
    </tbody>
</table>
</g:if>