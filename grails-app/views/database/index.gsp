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
    					<th>Table</th>
    					<th>Count</th>
    				</tr>
    			</thead>
    			<tbody>
    				<g:each var="table" in="${tables}">
    					<tr>
    						<td>${table.name}</td>
    						<td>${table.count}</td>
    					</tr>
    				</g:each>
    			</tbody>
    		</table>
    	</div>
    	<div class="container mt-4">
    		<div class="row">
    			<div class="col-lg-6">
    				<table class="display table table-striped table-bordered" style="width:100%">
		    			<thead>
		    				<tr>
		    					<th>Websites</th>
		    					<th>Products</th>
		    				</tr>
		    			</thead>
		    			<tbody>
		    				<g:each var="table" in="${websites}">
		    					<tr>
		    						<td>${table.name}</td>
		    						<td>${table.count}</td>
		    					</tr>
		    				</g:each>
		    			</tbody>
		    		</table>
    			</div>
    			<div class="col-lg-6">
    				<table class="display table table-striped table-bordered" style="width:100%">
		    			<thead>
		    				<tr>
		    					<th>Category Label</th>
		    					<th>Count</th>
		    				</tr>
		    			</thead>
		    			<tbody>
		    				<g:each var="table" in="${labels}">
		    					<tr>
		    						<td>${table.name}</td>
		    						<td>${table.count}</td>
		    					</tr>
		    				</g:each>
		    			</tbody>
		    		</table>
    			</div>
    		</div>
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


