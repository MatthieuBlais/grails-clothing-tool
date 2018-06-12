package db

class ApiRequests {

	String name 
	String description 
	String parameters 
	Boolean isUrgent

	Date createDate

    static constraints = {
    	parameters nullable:true, maxSize:2048
    	description maxSize:2048
    }

    ArrayList formatParameters(){
    	return parameters.split("\n")
    }
}
