<html lang="en" class="no-js">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <title>
        <g:layoutTitle default="Grails"/>
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>

    <asset:javascript src="vendors/pace/pace.min.js"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.16/css/dataTables.bootstrap4.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/1.5.1/css/buttons.dataTables.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <asset:stylesheet src="layout/main.css"/>

    <g:layoutHead/>
</head>
<body>


    <!-- MAIN NAVBAR -->
    <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark bg-navbar">
      <a class="navbar-brand mr-auto mr-lg-0" href="#">MeOw</a>
      <button class="navbar-toggler p-0 border-0" type="button" data-toggle="offcanvas">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="navbar-collapse offcanvas-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
          <g:render template="/layouts/navbar"></g:render>
        </ul>
        <ul class="navbar-nav my-2 my-lg-0">
            <li class="nav-item active mt-1 mr-3">
                <a class="nav-link" href="/help/index"><i class="fa fa-question-circle" aria-hidden="true"></i></a>
            </li>
            <li class="nav-item active bg-yellow">
                <a class="nav-link" href="/logout/index">Logout </a>
            </li>
        </ul>
        %{-- <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form> --}%
      </div>
    </nav>

    <!-- SUB NAVBAR -->
    <div class="nav-scroller bg-white box-shadow">
      <nav class="nav nav-underline">
        <a class="nav-link active" href="/${controllerName}/index">Home</a>
        <g:render template="/layouts/subnavbar"></g:render>
      </nav>
    </div>

    <main role="main" class="container">
        <g:layoutBody/>
    </main>

    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <asset:javascript src="layout/main.js"/>
    <g:pageProperty name="page.javascript"/>
</body>
</html>
