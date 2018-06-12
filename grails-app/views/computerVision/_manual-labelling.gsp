<div class="row">
	<div class="col-lg-8 col-md-8 col-sm-12">
		<div id="canvas">
			<img class="img-center img-responsive" style="max-height:500px;" src="/assets/placeholder.jpg" >
		</div>
	</div>
	<div class="col-lg-4 col-md-4 col-sm-12">
		<div class="text-center">
			<div class="btn-group" role="group" aria-label="Basic example" >
		  <button type="button" class="btn btn-secondary" id="previous-btn"><span class="fa fa-arrow-left"></span></button>
		  <button type="button" class="btn btn-success" id="save-btn">Save</button>
		  <button type="button" class="btn btn-danger" id="clear-button">Clear</button>
		  <button type="button" class="btn btn-secondary" id="next-btn"><span class="fa fa-arrow-right"></span></button>
		</div>
		</div>
		<div class="row mt-3">
			<strong>Coordinates: </strong><span id="coordinates-info"></span>
		</div>
		<div class="row mt-1">
			
			<div class="list-group" style="width: 100%;" id="label-list">
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('pants')? 'active':''}" data-value="pants" data-toggle="list">Pants</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('outerwears')? 'active':''}" data-value="outerwears" data-toggle="list">Outerwears</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('t-shirts')? 't-shirts':''}" data-value="t-shirts" data-toggle="list">T-Shirts</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('tops')? 'active':''}" data-value="tops" data-toggle="list">Tops</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('skirts')? 'active':''}" data-value="skirts" data-toggle="list">Skirts</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('shorts')? 'active':''}" data-value="shorts" data-toggle="list">Shorts</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('jeans')? 'active':''}" data-value="jeans" data-toggle="list">Jeans</a>
		  <a href="#" class="list-group-item list-group-item-action ${label?.equals('dresses')? 'active':''}" data-value="dresses" data-toggle="list">Dresses</a>
		</div>
		</div>
	</div>
</div>

<div class="container mt-5">
	<div class="row" id="gallery" style="height:300px; overflow-y:scroll;">
	</div>
</div>