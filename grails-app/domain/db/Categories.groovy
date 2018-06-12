package db

class Categories {

	String name
	String label
	Genders gender
	Categories category
    String altName

    static constraints = {
    	name nullable:false
    	label nullable:true
    	gender nullable:true
        altName nullable:true
    	category nullable:true
    }

    static mapping = {
		cache true
	}
}
