package db

class Server {

	String name 
	String type 
	String ip 

    static constraints = {
    	name maxSize:32
    	type maxSize:32
    	ip maxSize:16
    }

    static mapping = {
		cache true
	}
}
