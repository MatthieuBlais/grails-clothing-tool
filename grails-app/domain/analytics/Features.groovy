package db

class Features {

	String name

	static belongsTo = [group: FeatureGroups]
	static hasMany = [images: FeatureImages]

    static constraints = {
    	name maxSize:64
    }

    static mapping = {
		cache true
	}
}
