package db

class Prices {

    String id 

	String currency 
	Date createAt 
	Float value
	Boolean isDiscount

	static belongsTo = [product: Products]

    static constraints = {
    	id maxSize: 32, column: 'id'
    	currency nullable:false, maxSize:6
    	value nullable:false
    	isDiscount nullable:true
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}
}
