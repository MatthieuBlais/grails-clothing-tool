package db

import grails.transaction.Transactional

@Transactional
class ApplicationAPIService {

    def serviceMethod() {

    }

    def listEndpoints(){
    	return ApiEndpoints.list().groupBy({ endpoint -> endpoint.endpointGroup }).sort{ it.endpointGroup }
    }

    def listRequests(){
    	return ApiRequests.list().sort{ x,y ->  x.isUrgent == y.isUrgent ? x.createDate <=> y.createDate : x.isUrgent <=> y.isUrgent } 
    }

    def deleteRequest(id){
    	def req = ApiRequests.findById(id)
    	if(req) return !req.delete(flush:true, failOnError:true)
    	return false
    }

    def saveOrEditRequest(params){
    	def req = new ApiRequests(params)
    	if(params.id){
    		req = ApiRequests.findById(params.int('id'))
    		if(!req) return false
    		req.properties = params
    	}
    	req.createDate = new Date()
    	if(!params.isUrgent) req.isUrgent = false
    	return req.save(flush:true, failOnError:true)
    }

    def deleteEndpoint(id){
    	def endpoint = ApiEndpoints.findById(id)
    	if(endpoint) return !endpoint.delete(flush:true, failOnError:true )
    	return
    }

    def saveOrEditEnpoint(params){
    	def endpoint = new ApiEndpoints(params)
    	def paramsToDelete=[]
    	if(params.id){
    		endpoint = ApiEndpoints.findById(params.int('id'))
    		if(!endpoint) return false
    		endpoint.parameters.each{
    			paramsToDelete.add(it.id)
    		}
    		endpoint.properties = params
    	}
    	def parameters = params.paramsField.split("\n")
    	def all_params = []
    	parameters.each{
    		def data = it.split(",")
    		if(data.size()==5) all_params.add(new ApiParameters(name:data[0], type:data[1], title:data[2], description:data[3], mandatory:data[4].equals("mandatory"), endpoint:endpoint))
    	}
    	endpoint.parameters = all_params
    	endpoint.createDate = new Date()
    	if(endpoint.save(flush:true, failOnError:true)){
    		paramsToDelete.each{
    			ApiParameters.findById(it).delete(flush:true, failOnError:true)
    		}
    		return true
    	}
    	return false
    }
}