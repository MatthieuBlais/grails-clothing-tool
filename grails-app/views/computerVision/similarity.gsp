<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | Computer Vision</title>
  </head> 
  <body>


    <div class="container-fluid mt-5">
      <div class="col-lg-12">
        <form class="form-inline" id="similarity-form" action="similarity">
          <div class="form-group mb-2">
            <label for="algorithm" class="mr-2">Algorithm</label>
            <select class="form-control" id="algorithm" name="algorithm">
              <option value="basic">Get Started - Basic</option>
            </select>
          </div>
          <div class="form-group mx-sm-3 mb-2">
            <label for="type" class="mr-2">Type</label>
            <select class="form-control" id="type" name="type">
              <option value="shorts">Shorts</option>
            </select>
          </div>
          <div class="form-group mx-sm-3 mb-2">
            <label for="product" class="mr-2">Product ID</label>
            <input type="text" class="form-control" id="product" placeholder="Empty for random product">
          </div>
          <button type="submit" class="btn btn-primary mb-2">Find</button>
        </form>
      </div>
    </div>

    <g:if test="${product}">
      <div class="row">
         <div class="col-lg-6 ">
            <div class="container highlight p-3">
               <h6><a href="${product.url}">${product.name}</a></h6>
               <div>
                 <dt>ID: ${product.id}</dt>
                 <dd>WEBSITE: ${product.website.name}<br/>
                 PRICE: ${product?.currentPrice?.currency}${product?.currentPrice?.value} <g:if test="${product?.currentDiscount}">CURRENT DISCOUNT: ${product?.currentDiscount?.currency}${product?.currentDiscount?.value}</g:if></dd>
               </div>
               <div class="row p-2">
                 <g:each var="image" in="${product.images}">
                    <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6 p-1">
                      <img style="max-width:100%; max-height:300px;" src="${image.url}" class="img-responsive img-center img-gallery">
                    </div>
                 </g:each>
               </div>
            </div>
         </div>
         <div class="col-lg-6">
            <div class="container">
              <ul class="list-group">
                <g:each var="similarProduct" in="${similar}">
                  <li class="list-group-item">
                       <h6><a href="${product.url}">${similarProduct.product.name}</a></h6>
                       <div>
                         <dt>SCORE: ${similarProduct.score.score}</dt>
                         <dd>ID: ${similarProduct.product.id}<br/>
                         WEBSITE: ${similarProduct.product.website.name}<br/>
                         PRICE: ${similarProduct.product?.currentPrice?.currency}${similarProduct.product?.currentPrice?.value} <g:if test="${similarProduct.product?.currentDiscount}">CURRENT DISCOUNT: ${similarProduct.product?.currentDiscount?.currency}${similarProduct.product?.currentDiscount?.value}</g:if></dd>
                       </div>
                       <div class="row p-2">
                         <g:each var="image" in="${similarProduct.product.images}">
                            <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6 p-1">
                              <img style="max-width:100%; max" src="${image.url}" class="img-responsive img-center img-gallery">
                            </div>
                         </g:each>
                       </div>
                  </li>
                </g:each>
              </ul>
            </div>
         </div>
      </div>
    </g:if>

		<content tag="javascript">
			<asset:javascript src="components/async-loading.js"/>
		</content>
  </body>
</html>


