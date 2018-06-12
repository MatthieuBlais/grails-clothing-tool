<g:each var="image" in="${images}">
	<div class="col-lg-3 col-md-4 col-sm-6 col-xs-6 p-1 crop-container">
		<div class="crop" style="overflow: hidden; width:100%;">
			<img style="max-height:200px;" class="img-responsive img-center img-gallery new" src="${image.url}" data-id="${image.id}" data-xmin="${image.x_min}" data-xmax="${image.x_max}" data-ymin="${image.y_min}" data-ymax="${image.y_max}">
		</div>
	</div>
</g:each>
<span id="total" data-value="${total}"></span>