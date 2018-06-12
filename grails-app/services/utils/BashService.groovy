package db

import grails.transaction.Transactional

@Transactional
class BashService {

	def jsonService

    def serviceMethod() {

    }

    def getCurrentPath(){
    	  def directory = new File(".").getAbsoluteFile().getParent()
	      directory = directory.split("/")
	      def path=""
	      def found =false
	      directory.each{
	        path += it + "/"
	        if(it.equals("db")) found = true 
	      }
	      return path
    }

    /**
    *	Execute a bash command (linux)
    *	@attr bash is the bash command (ex: python)
    *	@attr path is the path of the script to execute (absolute paht)
    *	@attr parameter is a string. Call hashMapToParameter() to format it
    *	@output Hashmap. Your script must have a JSON format output. If not, you will get an error.
    **/
    def execute(bash, path, parameter){
        log.info bash+" "+path+" \'"+parameter+"\'"
        ProcessBuilder pb = new ProcessBuilder(bash, path,  parameter);
        Process process = pb.start();
        def result = new StringBuffer()
        def err = new StringBuffer()
        process.consumeProcessOutput( result, err )
        process.waitFor()
        log.info result.toString()
        log.info err.toString()
        //result='[{"series":[{"pointPadding":0,"pointPlacement":"between","type":"column","groupPadding":0,"data":[[0,1],[15,6],[30,17],[45,47],[60,113],[75,118],[90,107],[105,98],[120,232],[135,271],[150,304],[165,361],[180,241],[195,406],[210,221]],"name":"Customers"}],"retailgear":{"script":"/therow/customers/analysis/purchasefrequency.py","subtitle":"one purchase every X days","description":"Each column shows the number of customers who do a purchase less than every X days.","filters":[{"text":"Days between two purchases at ","key":"stores","mDefault":[-1],"type":"dropdown","options":[{"value":"all stores","key":-1},{"value":"WHS","key":0},{"value":"RGL","key":1},{"value":"STR","key":2},{"value":"FIM","key":3},{"value":"FCL","key":4},{"value":"SMN","key":5},{"value":"FFE","key":6},{"value":"FGA","key":7},{"value":"FCB","key":8},{"value":"902","key":9},{"value":"FSS","key":10},{"value":"SPM","key":11},{"value":"EER","key":18},{"value":"FMA","key":19},{"value":"FMM","key":20},{"value":"FMG","key":21},{"value":"SIP","key":24}],"isMultiple":true},{"text":" for members with at least ","type":"number","key":"treshold","value":1,"min":1},{"text":"purchase since ","type":"date","key":"period","value":"01 December, 2016"}],"title":"Purchase Frequency","header":false,"daterange":"Since 01 December, 2016","insight":{"buttons":[{"action":"/therow/customers/analysis/extractemailpurchasefrequency.py","text":"Get the list!","type":"GET","key":0,"color":"#0277BD"},{"action":"/therow/customers/analysis/extractemailpurchasefrequency.py","text":"Get the list!","type":"GET","key":1,"color":""}],"header":"It is time to remind them how great your products are!","text":"Click on the left button to get the email addresses and the purchase frequency of your members and on the right button to get the list of members who have not done any purchase since 01 December, 2016"},"type":"highcharts","size":{"width":"medium"}},"chart":{"type":"column"},"xAxis":{"gridLineWidth":1},"yAxis":{"title":{"text":"Number members"}}}]'
        return jsonService.parse(result.toString())
    }

    /**
    *	Format a hashmap in a string "KEY:VALUE|KEY:VALUE" that is used to execute a bash command
    *	@attr hashmap
    *	@output formatted string
    **/
    def hashMapToParameter(hashamp){
    	def _list = []
    	hashamp.each{ key, value -> 
    		_list.add(key+":"+value)
		}
		return _list.join("|")
    }

    def hashMapToJson(hashmap){
        return jsonService.toJson(hashmap)
    }
}
