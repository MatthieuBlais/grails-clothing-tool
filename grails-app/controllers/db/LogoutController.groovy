package db

import grails.converters.JSON
import grails.plugin.springsecurity.SpringSecurityUtils

class LogoutController {
	
	/**
	 * Dependency injection for the springSecurityService.
	 */
	def springSecurityService
	
	/**
	 * Index action. Redirects to the Spring security logout uri.
	 */
	def index(){
	   //redirect  controller:"Analytics",action:"aboutus"
	   println(SpringSecurityUtils.securityConfig.logout.filterProcessesUrl)
	   if(springSecurityService.getCurrentUser())
		{
			log.info('User Logout: ' + springSecurityService.getCurrentUser().id)
		}
		session.invalidate()
       //redirect uri: SpringSecurityUtils.securityConfig.logout.filterProcessesUrl // '/j_spring_security_logout'
       redirect url:'/login/auth'
	}
	
	/**
	 * Index action. Redirects to the Spring security logout uri.
	 */
	def ajaxLogout = {
		// TODO put any pre-logout code here
		
		render([success: true] as JSON)
	}
}
