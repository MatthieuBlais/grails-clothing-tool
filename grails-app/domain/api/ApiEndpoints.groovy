package db

class ApiEndpoints {

	String endpointGroup
	String endpoint
	String method 
	String function 
	String description

	String example 
	String output
	String errorCodes

	Date createDate
	Boolean deprecated

	static hasMany = [parameters: ApiParameters]

    static constraints = {
    	function nullable:true, maxSize:500
    	description nullable:true, maxSize:2048
    	createDate nullable:true
    	example nullable:true
    	output nullable:true, maxSize:5000
    	deprecated nullable:true
    	errorCodes nullable:true, maxSize:5000
    }

    static mapping = {
		cache true
	}

	String formatParameters(){
		def list = []
		parameters.each{
			def tmp = it.name+","+it.type+","+it.title+","+it.description+","+(it.mandatory?'mandatory':'')
			list.add(tmp)
		}
		return list.join("\n")
	}
}
