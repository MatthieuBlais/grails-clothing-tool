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
            <form action="/applicationAPI/saveEndpoint" method="POST">
              <g:if test="${endpoint?.id}"><input name="id" value="${endpoint?.id}"></g:if>
              <div class="form-group">
                <label for="endpointGroup">Group</label>
                <input type="text" class="form-control" id="endpointGroup" placeholder="API Group" name="endpointGroup" value="${endpoint?.endpointGroup}">
              </div>
              <div class="form-group">
                <label for="endpoint">Endpoint</label>
                <input type="text" class="form-control" id="endpoint" placeholder="Endpoint" name="endpoint" value="${endpoint?.endpoint}">
              </div>
              <div class="form-group">
                <label for="method">Method</label>
                <input type="text" class="form-control" id="method" placeholder="Method" name="method" value="${endpoint?.method}">
              </div>
              <div class="form-group">
                <label for="function">Short Description</label>
                <input type="text" class="form-control" id="function" placeholder="Short Description" name="function" value="${endpoint?.function}">
              </div>
              <div class="form-group">
                <label for="description">Description</label>
                <textarea class="form-control" name="description" rows="4">${endpoint?.description}</textarea>
              </div>
              <div class="form-group">
                <label for="paramsField">Parameters</label><br/>
                <small>Go to the next line for each parameter. Follow this notation: name,type,title,description,mandatory. Don't use comma in description.</small>
                <textarea class="form-control" name="paramsField" rows="8">${endpoint?.formatParameters()}</textarea>
              </div>
              <div class="form-group">
                <label for="example">Example:</label>
                <textarea class="form-control" name="example" rows="4">${endpoint?.example}</textarea>
              </div>
              <div class="form-group">
                <label for="output">Output</label>
                <textarea class="form-control" name="output" rows="6">${endpoint?.output}</textarea>
              </div>
              <div class="form-group">
                <label for="errorCodes">Error Codes</label>
                <textarea class="form-control" name="errorCodes" rows="6">${endpoint?.errorCodes}</textarea>
              </div>
              <div class="form-check">
                <input type="checkbox" class="form-check-input" id="deprecated" name="deprecated" ${request?.deprecated? "checked": ""}>
                <label class="form-check-label" for="deprecated">Deprecated</label>
              </div>
              <div class="form-group mt-3">
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
        </div>
    </div>

  </body>
</html>
