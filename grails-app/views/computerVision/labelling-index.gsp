<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | Database</title>
  </head>
  <body>
    <div class="container-fluid">
    	<div class="container mt-5">
    		<table class="display table table-striped table-bordered" style="width:100%">
    			<thead>
    				<tr>
    					<th>Label</th>
    					<th>Manual Count</th>
    					<th>Auto Count (Primary)</th>
                        <th>Auto Count (Secondary)</th>
    					<th>Auto Verified</th>
    				</tr>
    			</thead>
    			<tbody>
    				<g:each var="label" in="${labels}">
    					<tr>
    						<td>${label.name}</td>
    						<td>${label.manual}</td>
    						<td>${label.autoPrimary}</td>
                            <td>${label.autoSecondary}</td>
    						<td>${label.verified}</td>
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
			$("table").DataTable({
			      dom: 'Brt',
			      pageLength: 25
			  })
		})
		</script>
	</content>
  </body>
</html>


