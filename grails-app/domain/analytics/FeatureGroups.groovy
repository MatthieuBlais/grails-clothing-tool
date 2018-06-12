package db

class FeatureGroups {

	String name
	String label

	static hasMany = [features: Features]

    static constraints = {
    	name maxSize:64
    	label maxSize:32
    }

    static mapping = {
		cache true
	}
}
