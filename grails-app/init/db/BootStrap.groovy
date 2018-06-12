package db

import grails.util.GrailsUtil 
import grails.converters.JSON

import javax.servlet.http.HttpServletRequest

class BootStrap {

	def springSecurityService

    def init = { servletContext ->

    	//initUser()
    	initRequestMap()
    }
    def destroy = {
    }

    private void initRequestMap(){
    	Requestmap.executeUpdate( 'DELETE FROM Requestmap' )
        Requestmap.withSession {
            session ->
            session.clear()
        }

        //IS AUTHENTICATED ANONYMOUSLY (PERMITALL) 
        new Requestmap(url: '/website/*', configAttribute: 'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/gridfs/get', configAttribute: 'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/logout/*', configAttribute: 'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/login/*', configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/login/**', configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true)
        new Requestmap(url: '/j_spring_security_check', configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/js/**',configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/css/**',configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/static/**',configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/images/**',configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 
        new Requestmap(url: '/zkau/**',configAttribute:'IS_AUTHENTICATED_ANONYMOUSLY').save(flush:true, failOnError: true) 

        new Requestmap(url: '/home/**',configAttribute:'IS_AUTHENTICATED_REMEMBERED').save(flush:true, failOnError: true) 
        new Requestmap(url: '/home/**',configAttribute:'IS_AUTHENTICATED_FULLY').save(flush:true, failOnError: true)
        new Requestmap(url: '/database/**',configAttribute:'IS_AUTHENTICATED_FULLY,IS_AUTHENTICATED_REMEMBERED').save(flush:true, failOnError: true) 
        new Requestmap(url: '/computerVision/**',configAttribute:'IS_AUTHENTICATED_FULLY,IS_AUTHENTICATED_REMEMBERED').save(flush:true, failOnError: true) 
        new Requestmap(url: '/applicationAPI/**',configAttribute:'IS_AUTHENTICATED_FULLY,IS_AUTHENTICATED_REMEMBERED').save(flush:true, failOnError: true) 
        new Requestmap(url: '/help/**',configAttribute:'IS_AUTHENTICATED_FULLY,IS_AUTHENTICATED_REMEMBERED').save(flush:true, failOnError: true) 
    }

    private void initUser(){
        def email = "YOUR_EMAIL"
        def password = "YOUR_PASSWORD"

    	def sysUser = User.findByEmail(email) ?: new User(firstname:"Mr", lastname:"MeOw", username: email, email:email, password: springSecurityService.encodePassword(password) , profilePicture:"http://www.catster.com/wp-content/uploads/2017/09/A-gray-cat-meowing-with-his-mouth-open.jpg", enabled:true, accountExpired:false, accountLocked:false, passwordExpired:false).save(failOnError: true, flush:true)
	    def admin = Role.findOrSaveWhere(authority:'ROLE_MASTER',priority: 1).save(failOnError: true, flush:true)
    	UserRole.findOrSaveWhere(user:sysUser, role:admin).save(failOnError: true, flush:true)
    }

}
