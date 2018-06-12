package db

class FeatureImages {

	String url 
	String product
	Integer detectionId

    static constraints = {
    	url maxSize: 2048
    	product maxSize: 32
    }
}
