<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | Home</title>
  </head>
  <body>
  	<div class="container-fluid">
        <div class="container mt-5">
            <div class="row">
                <div class="col-lg-3 col-md-4 col-sm-12">
                    <strong>Reference:</strong><br/>
                    <ul>
                        <li><a href='#database'>Database</a>
                        <ul>
                          <li><a href='#database-overview'>Overview</a></li>
                          <li><a href='#database-crawlers'>Crawlers</a></li>
                          <li><a href='#database-sql'>SQL Queries</a></li>
                        </ul>
                        </li>
                        <li><a href='#computervision'>Computer Vision</a>
                        <ul>
                          <li><a href='#computervision-labelling'>Labelling</a></li>
                          <li><a href='#computervision-similarity'>Similarity</a></li>
                        </ul>
                        </li>
                        <li><a href='#api'>API</a>
                        <ul>
                          <li><a href='#api-request'>Request</a></li>
                          <li><a href='#api-endpoint'>Endpoint</a></li>
                        </ul>
                        </li>
                    </ul>
                </div>
                <div class="col-lg-9 col-md-8 col-sm-12">
                    <div class="container mt-5">
                            <h3>Help Section</h3>
                            <p>Please find the user manual below. If you don't understand, please message me. I will try to update it regularly but you can do it as well.</p>
                            <div class="container mt-5" id='database'>
                                <h4 id="database"><strong>Database</strong></h4>
                                    <h5 class="mt-4" id="database-overview">Overview</h5>
                                    <p>You can't do much here. It's only an overview of the products in the database.</p>
                                    <div class="alert alert-info" role="alert">
                                      The page might be long to load (5sec+) but it's because we use a very low price database (only 1 cpu).
                                    </div>
                                    <div class="col-lg-12">
                                      <img src="/assets/database-overview.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>
                                    
                                    <h5 class="mt-4" id="database-crawlers">Crawlers</h5>
                                    <p>Same, it's just an overview of the crawlers. We must develop a crawler for each website to grab their products, prices, etc... and it's not easy to maintain. Usually, when a website detects their is a robot scrapping the data, they block it and find ways to make it crash, especially with established companies (smaller retailers don't have the resources to fight against robots). Another reason a crawler can crash is when the html of a website is updated. The crawlers run everyday, so this page allows us to check if the crawler crashed or not by checking the number of products (SKU) that have been grabbed.</p>
                                    <p>Unique SKU is also important because it happened that one of the websites detected our robot but instead of making it crashed, it gave wrong data. If the difference between the number of skus and number of unique skus is too big, then there might be an issue.</p>
                                    <p>The stats are stored in DynamoDB, not in the main database</p>
                                    <div class="col-lg-12">
                                      <img src="/assets/database-crawlers.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>

                                    <h5 class="mt-4" id="database-sql">SQL Queries</h5>
                                    <p>This interface allows you to manually query the database to see the data. You can see it as a PSQL interface using the command line, but more user friendly. You can quickly load the product's table by clicking on the sub-navbard items.</p>
                                    <div class="alert alert-danger" role="alert">
                                      You query the live database! Be really careful if you use commands like DELETE and UPDATE!
                                    </div>
                                    <div class="col-lg-12">
                                      <img src="/assets/database-sql.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>

                                  <h4 id="computervision"><strong>Computer Vision</strong></h4>
                                    <h5 class="mt-4" id="computervision-labelling">Labelling</h5>
                                    <p>This interface allows you to manually label images and validate/verify the images that have been automatically labelled</p>
                                    <h6>Overview</h6>
                                    <p>The default page is an overview of the labelling task.</p>
                                    <ul>
                                      <li>Manual Count: Pictures manually labelled</li>
                                      <li>Auto Count (Primary): Pictures automatically labelled by a model. Primary means that the item was exepected. For example, if the model detects a dress in a picture that is supposed to have a dress, then it will be in the primary count.</li>
                                      <li>Auto Count (Secondary): Pictures automatically labelled by a model. However, this time, it's the case when the model detects a jeans whereas it was expected to find a t-shirt. The reason is that if you expect to detect a t-shirt, you're likely to see the bottom (jeans, pants) of the person in the picture and the model will detect it.</li>
                                      <li>Auto Verified: We can't trust the model yet, so we need to clean and validate the items that have been detected.</li>
                                    </ul>
                                    <div class="alert alert-info" role="alert">
                                      The page might be long to load because we use a very low price database (only 1 cpu) and a lot of data must be read.
                                    </div>
                                    <div class="col-lg-12">
                                      <img src="/assets/computervision-overview.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>
                                    <h6>Check labelling</h6>
                                    <p>You can see the images that have already been labelled with the three other options of the list: manually labelled, auto labelled (primary), auto labelled (secondary). </p>
                                    <div class="alert alert-danger" role="alert">
                                      Same here, please give time to the database to load your pictures...
                                    </div>
                                    <p>
                                      What you can do here is data cleaning. Each image is supposed to show an item that has been labelled. The goal here is to delete the pictures that show a jeans instead of a pants for example. Another use case is that the coordinates of the item are not very accurate, so you can update them through the interface
                                    </p>
                                    <p>
                                      <ul>
                                        <li>Delete: Click on the pictures you want to delete and click on "Delete"</li>
                                        <li>Coordinates update: Click on the pictures you want to update, adjust the coordinates with the arrows on the right. You must click on "save" to actually save your modifications</li>
                                      </ul> 
                                    </p>
                                    <div class="alert alert-info" role="alert">
                                      The automatic labelling is not completely done yet. <br/>
                                      You may have bugs as the cleaning part has just started
                                    </div>
                                    <div class="col-lg-12">
                                      <img src="/assets/computervision-verification.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>

                                    <h5 class="mt-4" id="computervision-similarity">Similarity</h5>
                                    <p>The main goal of the app is to find similar items right? Here will be the different similarity functions that will be developed. First, select an algorithm, select a type of product and click on "Find". If you want to check for a specific product, you can submit the product id, else, a random product is chosen.</p>
                                    <div class="alert alert-info" role="alert">
                                      For now, you have only the shorts because we need to clean the data first.
                                    </div>
                                    <div class="col-lg-12">
                                      <img src="/assets/computervision-similarity.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>

                                  <h4 id="api"><strong>API</strong></h4>
                                    <h5 class="mt-4" id="api-request">Request</h5>
                                    <p>You may need an API for what you're doing. You cannot query directly the database</p>
                                    <p>If you don't have an api endpoint yet, just create a new api request. Describe what you need (especially, what data you are expecting), and the parameters you need. Once, the backend is ready, the request will be deleted and you'll be able to see the endpoint on the endpoint's page.</p>
                                    <div class="alert alert-info" role="alert">
                                      Please use the shared database to do that. I can't see your request if you store them in your local database
                                    </div>
                                    <div class="col-lg-12">
                                      <img src="/assets/api-request.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>
                                    <h5 class="mt-4" id="api-endpoint">Endpoint</h5>
                                    <p>Official API documentation</p>
                                    <p>Just navigate through the documentation to find what you need. If something doesn't work as expected, create a new API request.</p>
                                    <div class="col-lg-12">
                                      <img src="/assets/api-endpoint.png" class="img-responsive img-center" style="max-width:100%" />
                                    </div>
                            </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    
  </body>
</html>


