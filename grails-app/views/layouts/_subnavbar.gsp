<g:if test="${controllerName.equals("database")}">
    <a class="nav-link" href="/database/queries?table=products">Products</a>
    <a class="nav-link" href="/database/queries?table=websites">Websites</a>
    <a class="nav-link" href="/database/queries?table=categories">Categories</a>
    <a class="nav-link" href="/database/queries?table=sizes">Sizes</a>
    <a class="nav-link" href="/database/queries?table=images">Images</a>
    <a class="nav-link" href="/database/queries?table=styles">Styles</a>
    <a class="nav-link" href="/database/queries?table=brands">Brands</a>
</g:if>
<g:if test="${controllerName.equals("computerVision") && actionName.equals('labelling')}">
    <a class="nav-link" href="/computerVision/labelling?label=pants">Pants</a>
    <a class="nav-link" href="/computerVision/labelling?label=outerwears">Outerwears</a>
    <a class="nav-link" href="/computerVision/labelling?label=tshirt">T-Shirts</a>
    <a class="nav-link" href="/computerVision/labelling?label=tops">Tops</a>
    <a class="nav-link" href="/computerVision/labelling?label=skirts">Skirts</a>
    <a class="nav-link" href="/computerVision/labelling?label=shorts">Shorts</a>
    <a class="nav-link" href="/computerVision/labelling?label=jeans">Jeans</a>
    <a class="nav-link" href="/computerVision/labelling?label=dress">Dresses</a>
</g:if>