package db

import groovy.sql.Sql

class DatabaseController {

	def dataSource
	def databaseService

    def index() {
        def tableStats = databaseService.getTableStats()
        def websiteStats = databaseService.getWebsiteStats()
        def labelStats = databaseService.getLabelStats()
        [tables:tableStats, websites:websiteStats, labels:labelStats]
    }

    def queries(){
        def table = databaseService.executeQuery(null, params.table)
        table + [query: params.table ? "SELECT * from "+params.table+" limit 200;" : ""]
    }

    def execute(){
    	def table = databaseService.executeQuery(params.query)
    	render(template:'sqlTable', model:table)
    }

    def crawlers(){
        [websites:databaseService.getLastRunStats(), airflowServer:Server.findByName("Airflow")]
    }
}
 