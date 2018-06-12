package db

import grails.converters.JSON;

class ApplicationAPIController {

	def applicationAPIService

    def index() { redirect(action:'endpoints')}

    def endpoints(){
    	[endpoints: applicationAPIService.listEndpoints()]
    }

    def requests(){
    	[requests: applicationAPIService.listRequests()]
    }

    def deleteRequest(String id){
    	applicationAPIService.deleteRequest(Integer.parseInt(id))
    	redirect(action:'requests')
    }

    def deleteEndpoint(String id){
    	applicationAPIService.deleteEndpoint(Integer.parseInt(id))
    	redirect(action:'endpoints')
    }

    def saveRequest(){
    	if(applicationAPIService.saveOrEditRequest(params)) redirect(action:'requests')
    	else render(view:'create-request', model:[request:new ApiRequests(params)])
    }

    def saveEndpoint(){
    	if(applicationAPIService.saveOrEditEnpoint(params)) redirect(action:'endpoints')
    	else render(view:'create-endpoint', model:[request:new ApiEndpoints(params)])
    }

    def createRequest(){
    	[request:new ApiRequests()]
    }

    def editRequest(String id){
    	render(view:'createRequest', model:[request:ApiRequests.findById(Integer.parseInt(id))])
    }

    def createEndpoint(){
    	[endpoint:new ApiEndpoints()]
    }

    def editEndpoint(String id){
    	render(view:'createEndpoint', model:[endpoint:ApiEndpoints.findById(Integer.parseInt(id))])
    }
}






