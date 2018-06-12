package db

class Images {

	String id

	String url
	String localStorage 
	String cloudStorage

	Boolean isMainPicture

	Boolean needProcess

	static belongsTo = [product: Products]

    static constraints = {
    	id maxSize: 32, column: 'id'
    	url nullable:false, maxSize:2048
    	localStorage nullable:true, maxSize:2048
    	cloudStorage nullable:true, maxSize:2048
    	isMainPicture nullable:true
    	needProcess nullable:true
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}

}



