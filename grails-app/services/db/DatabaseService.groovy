package db

import grails.transaction.Transactional
import groovy.sql.Sql

@Transactional
class DatabaseService {

	def dataSource
  def bashService

    def serviceMethod() {

    }

    def executeQuery(String query){
    	if(query==null) return [headers:[], rows:[]]
    	def sql = new Sql(dataSource)
      try {
        def results = sql.rows(query)
        if(results.size()==0) return [headers:[], rows:[]]
        def headers = []
        results[0].each{ k,v ->
          headers.add(k)
        }
        def rows = []
        results.each{
          def row = it
          def rowToAdd=[]
          headers.each{
            rowToAdd.add(row[it])
          }
          rows.add(rowToAdd)
        }
        return [headers:headers, rows:rows]
      }
      catch(Exception e) {
        return [headers:[], rows:[], error:e.getMessage()]
      }
    }

    def executeQuery(String query, String table){
    	if(table==null && query==null) return [headers:[], rows:[]]
    	if(query==null) query="SELECT * FROM "+table+" limit 150;"
    	def sql = new Sql(dataSource)
      try {
        def results = sql.rows(query)
        if(results.size()==0) return [headers:[], rows:[]]
        def headers = []
        results[0].each{ k,v ->
          headers.add(k)
        }
        def rows = []
        results.each{
          def row = it
          def rowToAdd=[]
          headers.each{
            rowToAdd.add(row[it])
          }
          rows.add(rowToAdd)
        }
        return [headers:headers, rows:rows]
      }
      catch(Exception e) {
        return [headers:[], rows:[], error:e.getMessage()]
      }
    }


    def getTableStats(){
      return [[name:"brands", count: Brands.count()], [name:"categories", count: Categories.count()], [name:"genders", count: Genders.count()], [name:"images", count: Images.count()], [name:"prices", count: Prices.count()], [name:"product_sizes", count: ProductSizes.count()], [name:"product_styles", count: ProductStyles.count()], [name:"products", count: Products.count()], [name:"sizes", count: Sizes.count()], [name:"styles", count: Styles.count()], [name:"websites", count: Websites.count()]]
    }

    def getWebsiteStats(){
      def websites = Websites.findAll()
      def output = []
      websites.each{
        output.add([name:it.name, count:Products.countByWebsite(it)])
      }
      return output
    }

    def getLabelStats(){
      def query = "SELECT c.alt_name as name, count(*) as count FROM categories c join products p on p.category_id = c.id group by c.alt_name"
      def sql = new Sql(dataSource)
      return sql.rows(query)
    }



    /**
    * CRAWLERS 
    **/

    def getLastRunStats(){
        def websites = Websites.findAll().name.unique()
        def currentPath = bashService.getCurrentPath()
        return bashService.execute("python", currentPath+"grails-app/scripts/crawlers-stats.py", bashService.hashMapToJson([websites:websites]))
    }
    
}
