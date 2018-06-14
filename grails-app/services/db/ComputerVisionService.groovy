package db

import grails.transaction.Transactional
import org.hibernate.criterion.CriteriaSpecification
import groovy.sql.Sql

@Transactional
class ComputerVisionService {

	def dataSource

    def serviceMethod() {

    }

    def loadImages(label, offset, isReview, isAuto, isPrimary){
        def sql = new Sql(dataSource)
        try {
            if(isReview){
                return loadDetections(label, isAuto, isPrimary, offset)
            }
            def manualOrAuto = isAuto ? 'is null' : '=true'
            def query = "SELECT i.url as url from (SELECT id from products where category_id in "+labelTranslation(label)+") p join images i on p.id = i.product_id where url not in (SELECT distinct url from object_detections where label = \'"+label+"\') order by url limit 100 offset "+offset
            def images = sql.rows(query)
            return images
        }
        catch(Exception e) {
            println e
            return []
        }
    }


    def loadImages2(label, offset, isReview, isAuto){
    	def sql = new Sql(dataSource)
		try {
			def isInOrNot = isReview ? '' : 'not'
            def manualOrAuto = isAuto ? 'is null' : '=true'
            def query = null
            if(isReview){
                query = "SELECT distinct url from object_detections where label = \'"+label+"\' and is_manual "+manualOrAuto+" order by url limit 100 offset "+offset
            }else{
                query = "SELECT i.url as url from (SELECT id from products where category_id in "+labelTranslation(label)+") p join images i on p.id = i.product_id where url "+isInOrNot+" in (SELECT distinct url from object_detections where label = \'"+label+"\' and is_manual "+manualOrAuto+") order by url limit 200 offset "+offset
            }
            def images = sql.rows(query)
			if(isInOrNot.isEmpty() && images.size()>0){
				def urls = []
				images.each{
					urls.add(it.url)
				}
				images = loadDetections(urls, label)
			}
			return images
		}
		catch(Exception e) {
			println e
			return []
		}
    }

    def loadDetections(label, isAuto, isPrimary, offset){
    	println isPrimary
        def manualOrAuto = isAuto ? 'is null' : '=true'
        def wasExpected = isPrimary ? '='+isPrimary : '=true'
    	def query="SELECT id, url, x_min, x_max, y_min, y_max, is_validated, is_wrong, condidence from object_detections where label = \'"+label+"\' and is_manual "+manualOrAuto+" and was_expected "+wasExpected+" order by url limit 100 offset "+offset
        //print query
    	//if(label) query+=" and label = \'"+label+"\'"
    	def sql = new Sql(dataSource)
    	try {
    		def detections = sql.rows(query)
    		return detections
    	}
    	catch(Exception e) {
			println e
			return []
		}
    }

    def labelTranslation(label){
        switch(label) {
            case 'tops':
                return '(168,100,79)'
            break
            case 'jeans':
                return '(45,56,101,122)'
            break
            case 'shorts':
                return '(52,104,81,106)'
            break
            case 'tshirt':
                return '(103,116,148,194,196,146,96)'
            break
            case 'skirts':
                return '(73,80,98)'
            break
            case 'pants':
                return '(82,178,195,83,18,84,105,121)'
            break
            case 'outerwears':
                return '(1,172,191,144,150,137,108,94,86,95,107,114,190,113)'
            break
            case 'dresses':
                return '(58,112)'
            break

        }
    }

    def saveLabel(originalLabel, label, src, xmin, ymin, xmax, ymax, width, height){
    	def objet = new ObjectDetections(url:src, xmin:normalize(xmin, width), xmax:normalize(xmax, width), ymin:normalize(ymin, height), ymax:normalize(ymax, height), label:label, condidence:100.0, wasExpected:originalLabel.equals(label), height:height, width:width, isValidated:true, isManual:true, detectionDate:new Date()).save(flush:true, failOnError:true)
    	return objet.id
    }

    def normalize(x, y){
    	if(y==0) return 0
    	return (float)x/(float)y
    }

    def deleteLabel(id){
    	def object = ObjectDetections.findById(id)
    	if(object) object.delete(flush:true, failOnError:true)
    }

    def getLabelStats(){
        def labels = ["jeans", "pants", "shorts", "skirts", "dress", "outerwears", "t-shirts", "tops"]
        def output = []
        labels.each{
            output.add([name:it, manual:ObjectDetections.countByLabelAndIsManual(it, true), autoPrimary: ObjectDetections.countByLabelAndIsManualAndWasExpected(it, null, true), autoSecondary: ObjectDetections.countByLabelAndIsManualAndWasExpected(it, null, false),  verified: ObjectDetections.countByLabelAndIsManualAndIsValidated(it, null, true)])
        }
        return output
    }

    def getValidatedStats(label, isManual){
        if(isManual) return ObjectDetections.countByLabelAndIsManual(label, true)
        else return ObjectDetections.countByLabelAndIsManualAndIsValidated(label, null, false)
    }

    def deleteDetections(ids){
        ids = ids.split(",")
        ids.each{
            def obj = ObjectDetections.findById(it)
            if(obj) obj.delete(flush:true, failOnError:true)
        }
    }

    def updateDetection(data){
        data = data.split("\\|")
        println data
        data.each{
            def objData = it.split(",")
            def obj = ObjectDetections.findById(Integer.parseInt(objData[0]))
            println objData
            obj.properties = [xmin:Float.parseFloat(objData[1]),xmax:Float.parseFloat(objData[2]),ymin:Float.parseFloat(objData[3]),ymax:Float.parseFloat(objData[4])]
            obj.save(flush:true, failOnError:true)
        }
    }

    def findSimilarItems(algorithm, itemType, productId){
        def productCount = SimilarityScores.countByProductType(itemType)
        if(productCount==0) return [product:null, similar:[]]
        if(!productId){
            def randomProductId = SimilarityScores.executeQuery('select product from SimilarityScores where productType = ? order by rand()', [itemType], [max: 1])
            productId = randomProductId[0]
        }
        println productId
        def similarItems = SimilarityScores.findAllByProduct(productId)
        println similarItems
        def mainProduct = Products.findById(productId) 
        def similarOutput = []
        similarItems.each{
            def product = Products.findById(it.similarProduct)
            similarOutput.add([product: product, score: it])
        }
        return [product: mainProduct, similar:similarOutput]
    }    
}



