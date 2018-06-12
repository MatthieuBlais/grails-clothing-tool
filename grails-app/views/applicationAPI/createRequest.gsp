<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | API</title>
  </head>
  <body>
    <div class="container-fluid">
        <div class="container mt-5">
            <form action="/applicationAPI/saveRequest" method="POST">
             <g:if test="${request?.id}"><input name="id" value="${request?.id}"></g:if>
              <div class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control" id="name" placeholder="name" name="name" value="${request?.name}">
              </div>
              <div class="form-group">
                <label for="description">Description</label>
                <textarea class="form-control" name="description" rows="4">${request?.description}</textarea>
              </div>
              <div class="form-group">
                <label for="parameters">Expected parameters</label><br/>
                <small>Go to the next line for each parameter. </small>
                <textarea class="form-control" name="parameters" rows="8">${request?.parameters}</textarea>
              </div>
              <div class="form-check">
                <input type="checkbox" class="form-check-input" id="isUrgent" name="isUrgent" ${request?.isUrgent? "checked": ""}>
                <label class="form-check-label" for="isUrgent">Need it quickly</label>
              </div>
              <div class="form-group mt-3">
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
        </div>
    </div>

  </body>
</html>

