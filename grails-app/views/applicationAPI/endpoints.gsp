<!DOCTYPE html>
<html lang="en">
  <head>
  <meta name='layout' content='main' />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MeOw | API</title>
    <style type="text/css">
    .highlight{
        background-color: #f7f7f9;
    }
    </style>
  </head>
  <body>
    <div class="container-fluid">
        <div class="container mt-5">
            <div class="row">
                <div class="col-lg-2 col-md-3 col-sm-12">
                    <strong>Reference:</strong><br/>
                    <ul>
                        <g:each var="endpoint" in="${endpoints}">
                            <li><a href='#${endpoint.key}'>${endpoint.key}</a></li>
                        </g:each>
                    </ul>
                    <g:if test='${endpoints.keySet().size()==0}'><i>Empty</i></g:if>
                </div>
                <div class="col-lg-10 col-md-9 col-sm-12">
                    <div class="container text-right">
                        <a class="btn btn-primary" href="/applicationAPI/createEndpoint">Create</a>
                    </div>
                    <div class="container mt-5">
                        <g:each var='endpoint' in='${endpoints}'>
                            <div class="container mt-5" id='${endpoint.key}'>
                                <h4><strong>${endpoint.key}</strong></h4>
                                <g:each var="function" in="${endpoint.value}">
                                    <h5 class="mt-4"><strong>${function.method} ${function.endpoint} <g:if test="${function.deprecated}"><i class="text-danger">Deprecated</i></g:if></strong><a role="button" style="float:right;" class="btn btn-danger btn-sm" href="/applicationAPI/deleteEndpoint/${function.id}"><i class="fa fa-times" aria-hidden="true"></i></a></h5>
                                    
                                    
                                    <p>${function.function} - <a role="button" class="btn btn-light btn-sm"  href="/applicationAPI/editEndpoint/${function.id}"><i class="fa fa-pencil" aria-hidden="true"></i></a></p>
                                    <p>${function.description}</p>
                                    <h6 class="mt-2"><strong>Parameters:</strong></h6>
                                    <g:if test='${function.parameters.size()==0}'>No params</g:if>
                                    <g:else>
                                        <table class="table table">
                                            <g:each var="parameter" in='${function.parameters}'>
                                                <tr>
                                                    <th>${parameter.name}<g:if test="${parameter.mandatory}"><span class="text-danger">*</span></g:if></th>
                                                    <td>${parameter.type}</td>
                                                    <td>${parameter.title}</td>
                                                    <td>${parameter.description}</td>
                                                </tr>
                                            </g:each>
                                        </table>
                                    </g:else>
                                    <h6 class="mt-2"><strong>Example:</strong></h6>
                                    <p><code>${function.example}</code></p>
                                    <h6><strong>Outpout Example:</strong></h6>
                                    <div class="highlight p-3"><pre type="JSON" class="mb-0" data-value="${function.output}"></pre></div>
                                    <g:if test="${function?.errorCodes}">
                                        <h6><strong>Error codes:</strong></h6>
                                        <ul class="highlight p-3">
                                            <g:each var="error" in="${function?.errorCodes?.split('\n')}">
                                                <li>${error}</li>
                                            </g:each>
                                        </ul>
                                    </g:if>
                                </g:each>
                            </div>
                        </g:each>
                    </div>
                </div>
            </div>
        </div>
    </div>

    
    <content tag="javascript">
        <script type="text/javascript">
        $(document).ready(function(){
            
            var jsons = $("pre[type=JSON]")
            for(var i=0; i<jsons.length;i++){
                $(jsons[i]).html(JSON.stringify($(jsons[i]).data('value'), undefined, 2))
            }

        })
        </script>
    </content>
  </body>
</html>