package db

import grails.transaction.Transactional

import groovy.json.JsonSlurper 
import groovy.json.JsonOutput


@Transactional
class JsonService {

    def serviceMethod() {

    }

    /**
    *	Parse a json string into hashmap component
    *	@input json string
    *	@output hashmap of json
    **/
    def parse(text){
        if(text==null || text.isEmpty()) return []
    	def jsonSlurper = new JsonSlurper()
    	try{
            return jsonSlurper.parseText(text)
      	}
	    catch(groovy.json.JsonException e){
	        return e.getMessage()
	    }
    }

    /**
    *   Format a map to json string
    *   @input hashmap
    *   @output json string
    **/
    def toJson(map){
        try{
            return JsonOutput.toJson(map)
        }catch(groovy.json.JsonException e){
            return e.getMessage()
        }
        
    }
    
}
