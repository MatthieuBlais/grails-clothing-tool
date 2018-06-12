package db

import grails.converters.JSON;

class ComputerVisionController {

	def computerVisionService

    def index() { redirect(action:'labelling') }

    def labelling(){
        if(params.label){
            [label:params.label]
        }else{
            def stats = computerVisionService.getLabelStats()
            render(view:'labelling-index', model:[labels:stats])
        }
    }

    def loadLabellingType(){
        if(params.type.equals('manual')) render(template:'manual-labelling')
        else render(template:'validation-labelling')
    }

    def loadImages(){
    	def images = computerVisionService.loadImages(params.label, params.offset, params.type, params.auto, params.isprimary)
        if(!params.type) render(template:'image-grid', model:[images:images, offset:params.int('offset')])
        else render(template:'validation-image-grid', model:[images:images, offset:params.int('offset'), total: computerVisionService.getValidatedStats(params.label, !params.auto)])
    }
 
    def saveLabelling(){
    	def id = computerVisionService.saveLabel(params.original, params.label, params.src, params.int('xmin'), params.int('ymin'), params.int('xmax'), params.int('ymax'), params.int('width'), params.int('height'))
    	render([success:true, id:id] as JSON)
    }

    def deleteLabel(){
    	computerVisionService.deleteLabel(params.id)
    	render([success:true] as JSON)
    }

    def deleteDetection(){
        computerVisionService.deleteDetections(params.ids)
        render([success:true] as JSON)
    }

    def updateDetection(){
        computerVisionService.updateDetection(params.data)
        render([success:true] as JSON)
    }


    def similarity(){
        if(params.algorithm && params.type){
            computerVisionService.findSimilarItems(params.algorithm, params.type, params.product)
        }
    }
}
