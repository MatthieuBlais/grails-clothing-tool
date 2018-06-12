<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | Computer Vision</title>
    <style type="text/css">
    .rectangle {
    border: 1px solid #dc3545;
    position: absolute;
}
    .saved.rectangle{
      border: 1px solid #28a745;
    position: absolute;
    }
    .guessed.rectangle{
      border: 1px solid #ffc107;
    position: absolute;
    }
    .img-gallery{
    	cursor: pointer;
    }

    .img-gallery.labelled{
    	border: 4px solid blue;
    }
    .img-gallery.active{
    	border: 4px solid green;
    }
    .crop-container.active{
      border: 2px solid green;
    }
  </style>
  </head> 
  <body>
    	<span id="label" data-value="${label}"></span>
  		<div class="container-fluid mt-5">
  			<div class="row">
  				<div class="col-lg-2 col-md-2 col-sm-12">
  					<div class="list-group" id="labelling-type">
					  <a href="#" class="list-group-item list-group-item-action active" data-toggle="list" data-value="manual">
					    Manual
					  </a>
					  <a href="#" class="list-group-item list-group-item-action" data-toggle="list" data-value="manual-saved">
					    Manual - Saved
					  </a>
					  <a href="#" class="list-group-item list-group-item-action" data-toggle="list" data-value="auto-primary">Auto (Primary)</a>
            <a href="#" class="list-group-item list-group-item-action" data-toggle="list" data-value="auto-secondary">Auto (Secondary)</a>
					</div>
  				</div>
  				<div class="col-lg-10 col-md-10 col-sm-12" id="labelling-container">
  					
  					
  				</div>
  			</div>
  		</div>

		<content tag="javascript">
			<asset:javascript src="components/drawer.js"/>
			<asset:javascript src="components/async-loading.js"/>
			<asset:javascript src="pages/labelling.js"/>
			<script type="text/javascript">
				$(document).ready(function(){
	                
					var type = $("#labelling-type .list-group-item-action.active")
					$.ajax({url: '/computerVision/loadLabellingType', data:{ type: $(type).data("value") }, method: "POST", success: function(result){ 
							$("#labelling-container").html(result)
							if($(type).data("value")=="manual") manualLabelling.init() 
			        	}
			    	});

					$("#labelling-type .list-group-item-action").click(function(){
						if(type != this){
							type = $(this)
							$.ajax({url: '/computerVision/loadLabellingType', data:{ type: $(type).data("value") }, method: "POST", success: function(result){ 
    									$("#labelling-container").html(result)
    									if($(type).data("value")=="manual") manualLabelling.init() 
                      if($(type).data("value")=="manual-saved") validationLabelling.init()
                      if($(type).data("value")=="auto-primary" || $(type).data("value")=="auto-secondary") validationLabelling.init()
					        	}
					    	});
						}
					})
					

	            })

	            



			</script>
		</content>
  </body>
</html>


