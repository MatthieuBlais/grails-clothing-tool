package db

import grails.plugin.springsecurity.SpringSecurityUtils
import javax.servlet.http.HttpServletResponse

import org.springframework.security.access.annotation.Secured
import org.springframework.security.authentication.AccountExpiredException
import org.springframework.security.authentication.CredentialsExpiredException
import org.springframework.security.authentication.DisabledException
import org.springframework.security.authentication.LockedException

import org.springframework.security.core.Authentication
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.security.web.WebAttributes
import java.security.SecureRandom

import org.apache.commons.codec.binary.Base64;
import java.text.SimpleDateFormat;
import grails.converters.JSON;
import groovy.sql.Sql

import java.security.MessageDigest
import java.net.URLEncoder;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import static grails.async.Promises.*
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import grails.core.GrailsApplication



class LoginController {

	def springSecurityService
	def authenticationTrustResolver

    def index() { 
    	if (springSecurityService.isLoggedIn()) {
			def currentUser = springSecurityService.getCurrentUser()
			log.info(""+currentUser.id+" JUST LOGGED IN")
			session['user'] = currentUser
			
			//def plugins = springSecurityService.getCurrentUser().company.settings?.getListPlugins()
			//session.plugins = [list:plugins!=null? plugins : [], active: plugins!=null? plugins[0] : null]
			redirect action: 'index', controller: 'home'
		}
		else {
			log.error("Authentication failed")
			redirect action: 'auth', params: params
		}
    }

    /** Show the login page. */
	def auth() {
		def config = SpringSecurityUtils.securityConfig
		if (springSecurityService.isLoggedIn()) {
			redirect uri: config.successHandler.defaultTargetUrl
			return
		}
		String view = 'auth'
		String postUrl = "${request.contextPath}${config.apf.filterProcessesUrl}"
		log.info postUrl
		if(request.xhr) render(template:"login", model:[postUrl: postUrl, rememberMeParameter: config.rememberMe.parameter, hasCookie: authenticationTrustResolver.isRememberMe(authentication)])
		else render view: 'auth', model: [postUrl: postUrl, rememberMeParameter: config.rememberMe.parameter, hasCookie: authenticationTrustResolver.isRememberMe(authentication)]
	}

	/** The redirect action for Ajax requests. */
	def authAjax() {
		response.setHeader 'Location', SpringSecurityUtils.securityConfig.auth.ajaxLoginFormUrl
		response.sendError HttpServletResponse.SC_UNAUTHORIZED
	}

	/** Show denied page. */
	def denied() {
		if (springSecurityService.isLoggedIn() && authenticationTrustResolver.isRememberMe(authentication)) {
			// have cookie but the page is guarded with IS_AUTHENTICATED_FULLY (or the equivalent expression)
			redirect action: 'full', params: params
		}
		else{
			render view: 'denied'
		}
	}

	/** Login page for users with a remember-me cookie but accessing a IS_AUTHENTICATED_FULLY page. */
	def full() {
		def config = SpringSecurityUtils.securityConfig
		render view: 'auth', params: params,
		model: [hasCookie: authenticationTrustResolver.isRememberMe(authentication),
		postUrl: request.contextPath + config.apf.filterProcessesUrl]
	}

	/** Callback after a failed login. Redirects to the auth page with a warning message. */
	def authfail() {
		String msg = ''
		def exception = session[WebAttributes.AUTHENTICATION_EXCEPTION]
		log.error("Authentication failed: "+exception)
		if (exception) {
			if (exception instanceof AccountExpiredException) {
				msg = g.message(code: "springSecurity.errors.login.expired")
			}
			else if (exception instanceof CredentialsExpiredException) {
				msg = g.message(code: "springSecurity.errors.login.passwordExpired")
			}
			else if (exception instanceof DisabledException) {
				msg = g.message(code: "springSecurity.errors.login.disabled")
			}
			else if (exception instanceof LockedException) {
				msg = g.message(code: "springSecurity.errors.login.locked")
			}
			else {

				msg = g.message(code: "springSecurity.errors.login.fail")
			}
		}
		if (springSecurityService.isAjax(request)) {
			println "HELLO"
			println msg
			render([error: msg] as JSON)
		}
		else {
			println "HI"
			flash.error = exception.message
			println exception.message
			redirect action: 'auth', params: params
		}
	}

	/** The Ajax success redirect url. */
	def ajaxSuccess() {
		render([success: true, username: springSecurityService.authentication.name] as JSON)
	}

	/** The Ajax denied redirect url. */
	def ajaxDenied() {
		println "DENIED"
		render([error: 'access denied'] as JSON)
	}

	protected Authentication getAuthentication() {
		SecurityContextHolder.context?.authentication
	}


}
