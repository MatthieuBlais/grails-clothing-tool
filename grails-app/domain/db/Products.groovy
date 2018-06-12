package db

class Products {

	String id 

	Categories category
	Categories subcategory

	String sku 
	String name
	Genders gender
	Brands brand 
	Websites website

	Date createAt
	Date updateAt 

	String color
	String description 
	String generatedDescription 

	String url 

	Prices currentPrice
	Prices currentDiscount

	String styleLine

	Boolean needAdditionalData 
	Boolean needProcess 

	static hasMany = [images: Images, prices:Prices, discounts:Prices, sizes: ProductSizes, styles:ProductStyles]


    static constraints = {
    	id maxSize: 32, column: 'id'
		subcategory nullable:true
		sku maxSize: 128
		gender nullable:true
		brand nullable:true
		website nullable:true
		updateAt nullable:true
		description maxSize:2048, nullable:true
		generatedDescription maxSize:2048, nullable:true
		url maxSize:2048, nullable:true
		currentPrice nullable:true 
		currentDiscount nullable:true
		color nullable:true, maxSize:48
		styleLine nullable:true, maxSize:2048
		needAdditionalData nullable:true
		needProcess nullable:true 
    }

    static mapping = {
		id	generator:'uuid'
		cache true
	}
}