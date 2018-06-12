package db

class ObjectDetections {

    String url 
	String localPath 
	String cloudStorage
	String croppedName
	String noBackgroundPath

	Float xmin
	Float xmax
	Float ymin
	Float ymax 

	String label
	Float condidence
	Boolean wasExpected

	Float height
	Float width 

	Boolean isValidated 
	Boolean isWrong 
	Boolean isManual

	Date detectionDate

    static constraints = {
    	url nullable:true, maxSize:2048
		localPath nullable:true, maxSize:2048
		cloudStorage nullable:true, maxSize:2048
		croppedName maxSize:2048, nullable:true
		isValidated nullable:true
		isWrong nullable:true
		xmin column: 'x_min'
		xmax column: 'x_max'
		ymin column: 'y_min'
		ymax column: 'y_max'
		isManual nullable:true
		noBackgroundPath nullable:true, maxSize:2048
    }

    static mapping = {
		cache true
	}
}
