<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | API</title>
    <style type="text/css">
        .details-control{
            cursor: pointer;
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
  </head>
  <body>
    <div class="container-fluid">
        <div class="container mt-5">
            <a class="btn btn-primary" href="/applicationAPI/createRequest">Create</a>
        </div>
    	<div class="container mt-3">
    		<table class="display table table-striped table-bordered" style="width:100%">
    			<thead>
    				<tr>
    					<th>Last Update</th>
    					<th>Name</th>
    					<th>Description</th>
    					<th>Parameters</th>
                        <th></th>
    				</tr>
    			</thead>
    			<tbody>
    				<g:each var="request" in="${requests}">
    					<tr>
    						<td><g:formatDate format="yyyy-MM-dd" date="${request.createDate}"/></td>
    						<g:if test='${request.isUrgent}'><td class="text-danger">${request.name}</td></g:if><g:else><td>${request.name}</td></g:else>
    						<td>${request.description}</td>
    						<td>
                                <ul>
                                    <g:each var="param" in="${request.formatParameters()}" status="i">
                                        <g:if test="${i<3}"><li>${param}</li></g:if>
                                    </g:each>
                                     <g:if test="${request.formatParameters().size()>2}"><li>...</li></g:if>
                                </ul>                  
                            </td>
                            <td>
                                <a role="button" class="btn btn-light" href="/applicationAPI/editRequest/${request.id}"><i class="fa fa-pencil" aria-hidden="true"></i></a>
                                <a role="button" class="btn btn-danger delete-request" href="/applicationAPI/deleteRequest/${request.id}"><i class="fa fa-times" aria-hidden="true"></i></a>
                            </td>
    					</tr>
    				</g:each>
    			</tbody>
    		</table>
    	</div>
    </div>

    
	<content tag="javascript">
		<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
		<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap4.min.js"></script>
		<script type="text/javascript">
		$(document).ready(function(){
			var table = $("table").DataTable({
			      dom: 'Blfrtip',
			      pageLength: 25,
                  "ordering": false,
                  "columns": [
                    {
                        "data":      'date'
                    },
                    { "data": "name" },
                    { "data": "description", "className": 'details-control' },
                    { "data": "parameters", "className": 'details-control' },
                    { "data": "action" }
                ],
			  })

            $('table').on('click', 'td.details-control', function () {
                var tr = $(this).closest('tr');
                var row = table.row( tr );
         
                if ( row.child.isShown() ) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    // Open this row
                    row.child( format(row.data()) ).show();
                    tr.addClass('shown');
                }
            } );


		})

        function format ( d ) {
            return '<strong>Description:</strong><br/>'+d.description+'<br/><br/>'+
                '<strong>Parameters:</strong><br/>'+d.parameters;
        }
		</script>
	</content>
  </body>
</html>