package db

class Brands {

	String name 
	String type 

    static constraints = {
    	name nullable:false
    	type nullable:true
    }

    static mapping = {
		cache true
	}
}
