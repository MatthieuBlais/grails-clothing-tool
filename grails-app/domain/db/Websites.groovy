package db

class Websites {

	String id

	String name
	String url 

    static constraints = {
    	id maxSize: 32, column: 'id'
    	name nullable:false 
    	url nullable:true, maxSize:2048
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}
}
