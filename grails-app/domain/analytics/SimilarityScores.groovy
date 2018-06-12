package db

class SimilarityScores implements Serializable {

    String product
	String similarProduct

	Float score 

	SimilarityFunctions similarityFunction
	String productType

    static constraints = {
    	product maxSize:32
		similarProduct maxSize:32
		score nullable:true
		productType nullable:true, maxSize:32
    }

    static mapping = {
		cache true
		id composite:['product', 'similarProduct'] 
	}
}
