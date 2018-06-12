package db

class ProductStyles {

	String id
	Styles style 
	Boolean isGenerated

	static belongsTo = [product: Products]

    static constraints = {
    	id maxSize: 32, column: 'id'
    	isGenerated nullable:true
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}
}
