<g:each var="image" in="${images}" status="i">
	<div class="col-lg-2 col-md-3 col-sm-4 col-xs-6 p-1">
		<img style="max-width:100%;" src="/assets/placeholder.jpg" data-src="${image.url}" class="img-responsive img-center img-gallery new" data-counter="${i+offset}">
	</div>
</g:each>
<div class="col-lg-2 col-md-3 col-sm-4 col-xs-6 p-1 mt-5 text-center load-more">
	<button class="btn btn-default">Load More</button>
</div>