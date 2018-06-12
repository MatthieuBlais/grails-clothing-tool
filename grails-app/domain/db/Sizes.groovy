package db

class Sizes {

	String id

	String name 
	String type 

    static constraints = {
    	id maxSize: 32, column: 'id'
    	name nullable:false, maxSize:64
    	type nullable:true
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}
}
