<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | Crawlers</title>
    <style type="text/css">
        .details{
            cursor: pointer;
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
  </head>
  <body>
    <div class="container-fluid mt-5">
        <h4>Scheduler</h4>
        <p>Airflow Management Console: <a href="http://${airflowServer.ip}:8585" target="_blank">${airflowServer.ip}:8585</a></p>
        <p>Airflow SSH Server: ec2-user@${airflowServer.ip}</p>
    	<div class="container mt-3">
    		<table class="display table table-striped table-bordered" style="width:100%">
    			<thead>
    				<tr>
                        <th>Website</th>
    					<th>Start</th>
    					<th>End</th>
    					<th>Total Skus</th>
                        <th>Unique Skus</th>
                        <th>Sku Details</th>
                        <th class="d-none"></th>
    				</tr>
    			</thead>
    			<tbody>
    				<g:each var="website" in="${websites}">
    					<tr>
    						<td>${website.website_id}</td>
    						<td>${website.start}</td>
    						<td>${website.stop}</td>
    						<td>${website.total}</td>
                            <td>${website.skus}</td>
                            <td>
                                <g:each var="k" in="${website.categories.keySet()}" status='i'>
                                    <g:if test="${i<2}"><li>${k}: ${website.categories[k]}</li></g:if>
                                    <g:if test="${i==2}"><li>...</li></g:if>
                                </g:each>
                            </td>
                            <td class="d-none">
                                <g:each var="k" in="${website.categories.keySet()}" status='i'>
                                    <li>${k}: ${website.categories[k]}</li>
                                </g:each>
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
                        "data":      'website'
                    },
                    { "data": "start" },
                    { "data": "stop" },
                    { "data": "total" },
                    { "data": "skus" },
                    { "data": "details", "className": 'details' },
                    { "data": "categories" }
                ],
			  })

            $('table').on('click', 'td.details', function () {
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
            return d.categories
        }
		</script>
	</content>
  </body>
</html>