package db

class ProductSizes {

	String id

	Sizes size
	Boolean available

	static belongsTo = [product: Products]

    static constraints = {
    	size nullable:false 
    	available nullable:true
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}
}
