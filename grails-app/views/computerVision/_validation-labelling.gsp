<div class="row">
	<div class="col-lg-8 col-md-8 col-sm-12">
		<div class="row" id="gallery" style="max-height:800px; overflow-y:scroll;">
		</div>
	</div>
	<div class="col-lg-4 col-md-4 col-sm-12">
		<div class="text-center">
			<div class="btn-group" role="group" aria-label="Basic example" >
			  <button type="button" class="btn btn-info" id="unselect-button">Unselect</button>
			  <button type="button" class="btn btn-success" id="save-btn">Save</button>
			  <button type="button" class="btn btn-danger" id="delete-button">Delete</button>
			</div>
		</div>
		<div class="row mt-4 ml-3">
			<strong>Selected: </strong><span id="selected-info"></span>
		</div>
		<div class="row mt-2">
			<div class="col-lg-6 col-md-6 col-sm-12 pr-0">
				<div class="card">
				  <div class="card-body">
				    <h5 class="card-title"><strong>TOP</strong></h5>
				    <div class="btn-group" role="group" aria-label="Basic example" >
					  <button type="button" class="btn btn-secondary crop-button" data-type="top-up" data-name="up" data-counter="0"><span class="fa fa-chevron-up"></span></button>
					  <button type="button" class="btn btn-secondary crop-button" data-type="top-down" data-name="down" data-counter="0"><span class="fa fa-chevron-down"></span></button>
					</div>
				  </div>
				</div>
			</div>
			<div class="col-lg-6 col-md-6 col-sm-12 pl-0">
				<div class="card">
				  <div class="card-body">
				    <h5 class="card-title"><strong>BOTTOM</strong></h5>
				    <div class="btn-group" role="group" aria-label="Basic example" >
					  <button type="button" class="btn btn-secondary crop-button" data-type="bottom-up" data-name="up" data-counter="0"><span class="fa fa-chevron-up"></span></button>
					  <button type="button" class="btn btn-secondary crop-button" data-type="bottom-down" data-name="down" data-counter="0"><span class="fa fa-chevron-down"></span></button>
					</div>
				  </div>
				</div>
			</div>
			<div class="col-lg-6 col-md-6 col-sm-12 pr-0">
				<div class="card">
				  <div class="card-body">
				    <h5 class="card-title"><strong>LEFT</strong></h5>
				    <div class="btn-group" role="group" aria-label="Basic example" >
					  <button type="button" class="btn btn-secondary crop-button" data-type="left-left" data-name="left" data-counter="0"><span class="fa fa-chevron-left"></span></button>
					  <button type="button" class="btn btn-secondary crop-button" data-type="left-right" data-name="right" data-counter="0"><span class="fa fa-chevron-right"></span></button>
					</div>
				  </div>
				</div>
			</div>
			<div class="col-lg-6 col-md-6 col-sm-12 pl-0">
				<div class="card">
				  <div class="card-body">
				    <h5 class="card-title"><strong>RIGHT</strong></h5>
				    <div class="btn-group" role="group" aria-label="Basic example" >
					  <button type="button" class="btn btn-secondary crop-button" data-type="right-left" data-name="left" data-counter="0"><span class="fa fa-chevron-left"></span></button>
					  <button type="button" class="btn btn-secondary crop-button" data-type="right-right" data-name="right" data-counter="0"><span class="fa fa-chevron-right"></span></button>
					</div>
				  </div>
				</div>
			</div>
		</div>
		<div class="col-lg-12 text-center mt-4 ml-3">
			<div><strong>Total: </strong><span id="offset-info"></span>/<span id="total-info"></span></div>
			<div class="mt-2"><button type="button" class="btn btn-outling-secondary load-more">Load More</button></div>
		</div>
	</div>
</div>