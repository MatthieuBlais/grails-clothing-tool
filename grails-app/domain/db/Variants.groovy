package db

class Variants {

	String variantId 
	String size 
	String color 
	String productId

    static constraints = {
    	size maxSize:64, nullable:true
    	color maxSize:32, nullable:true
    	productId maxSize:32, nullable:true
    }

    static mapping = {
		cache true
	}
}
