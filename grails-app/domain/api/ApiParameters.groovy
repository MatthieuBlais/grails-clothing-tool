package db

class ApiParameters {

	String name
	String type 
	String title
	String description
	Boolean mandatory
	

	static belongsTo = [endpoint: ApiEndpoints]

    static constraints = {
    	description nullable:true, maxSize:2048
    	
    }
}
