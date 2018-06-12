<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | Database</title>
    
    <style type="text/css">
    	#editorContainer{
			position: relative;
			width: 100%;
			height: 200px;
		}
		#editor {
	        margin: 0;
	        position: absolute;
	        top: 0;
	        bottom: 0;
	        left: 0;
	        right: 0;
	    }
    </style>

  </head>
  <body>
    	<div id="editorContainer" class="container mt-4">
			<pre id="editor">${query}</pre>
		</div>
		<a data-toggle="collapse" href="#collapseHistory" role="button" aria-expanded="false" aria-controls="collapseHistory"><small>History</small></a>
		<div class="float-right mt-2"><button class="btn btn-primary my-2 my-sm-0" id="execute-sql" data-loading-text="<i class='fa fa-circle-o-notch fa-spin'></i>" data-text="Execute" style="width:84px; height:38px;">Execute</button></div>
		<div class="clearfix"></div>
		<div class="collapse mt-2" id="collapseHistory" style="max-height:200px; overflow-y: scroll;">
		  <div class="list-group" id="history-queries">
			  
			</div>
		</div>

		<div id="table-container" class="mt-4">
			<g:render template="sqlTable"></g:render>
		</div>

		
		<content tag="javascript">
			<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
			<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap4.min.js"></script>
			<script type="text/javascript" src='https://cdn.datatables.net/buttons/1.5.1/js/dataTables.buttons.min.js'></script>
			<script type="text/javascript" src='https://cdn.datatables.net/buttons/1.5.1/js/buttons.html5.min.js'></script>
			
			<asset:javascript src="vendors/ace/ace.js"/>
			<asset:javascript src="vendors/ace/ext-language_tools.js"/>
			<script type="text/javascript">
				ace.require("ace/ext/language_tools");
		    var editor = ace.edit("editor");
		    editor.session.setMode("ace/mode/sql");
		    editor.setTheme("ace/theme/textmate");
		    // enable autocompletion and snippets
		    editor.setOptions({
		        enableBasicAutocompletion: true,
		        enableSnippets: true,
		        enableLiveAutocompletion: true
		    });

		    editor.commands.addCommand({
	        name: "executeQuery",
	        bindKey: {win: "Ctrl-Enter", mac: "Command-Enter"},
	        exec: function(editor) {
	        		executeQuery(editor)
	        	}
	    	})

	    	$(document).ready(function(){
	    		$("#sql-table").DataTable({
				      dom: 'Blfrtip',
				      pageLength: 25,
				      buttons: [
				          'csv'
				      ],
				      "scrollX": true
				  })

	    		$("#execute-sql").click(function(){
	    			executeQuery(editor)
	    		})
	    	})

	    	function executeQuery(editor){
	    		$("#execute-sql").html($("#execute-sql").data("loading-text"))
	    		var query = editor.getValue();
        		$.ajax({url: '/database/execute', data:{ query: query }, method: "POST", success: function(result){
	                	 $("#table-container").html(result)
	                	 $("#execute-sql").html($("#execute-sql").data("text"))
	                	 addToHistoryList(query)
	                	 if($("#sql-table").length > 0){
	                	 	$("#sql-table").DataTable({
							      dom: 'Blfrtip',
							      pageLength: 25,
							      buttons: [
							          'csv'
							      ],
				      			"scrollX": true
							  })
        				 }
	                	 
	            	}
	        	});
	    	}


	    	function addToHistoryList(query){
	    		var all = query.split("\n");
	    		var last_query = "";
	    		for(var i=0; i<all.length; i++){
	    			if(!all[i].startsWith("--")){
	    				last_query = all[i]
	    			}
	    		}
	    		if(last_query!=""){
	    			$("#history-queries").prepend('<a href="#" class="list-group-item list-group-item-action new-history">'+last_query+'</a>')
	    			$(".new-history").click(function(){
	    				editor.setValue($(this).text());
	    			})
	    			$(".new-history").removeClass("new-history")
	    		}
	    	}

			</script>
		</content>
  </body>
</html>


