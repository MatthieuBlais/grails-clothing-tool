package db


import org.springframework.http.HttpMethod

import groovy.transform.EqualsAndHashCode
import groovy.transform.ToString
import grails.compiler.GrailsCompileStatic

@GrailsCompileStatic
@EqualsAndHashCode(includes=['configAttribute', 'httpMethod', 'url'])
@ToString(includes=['configAttribute', 'httpMethod', 'url'], cache=true, includeNames=true, includePackage=false)
class Requestmap implements Serializable {

	private static final long serialVersionUID = 1

	String  id
	String configAttribute
	HttpMethod httpMethod
	String url

	Set<String> getAuthorities() {
		configAttribute.split(",") as Set<String>
	}

	boolean hasAuthority(String authority){
		return configAttribute.split(",").contains(authority)
	}

	static constraints = {
		configAttribute blank: false
		httpMethod nullable: true
		url blank: false, unique: 'httpMethod'
		id 	maxSize:32, column:'id'
	}

	static mapping = {
		id 			generator:'uuid'
		id			column:'requestmap_id'
		cache true
		url			column:'requestmap_url',index:'requestmap_url_idx'
	}


	// static search = {
	// 	id			index:'un_tokenized'
	// 	url			index:'un_tokenized'
	// 	configAttribute index:'un_tokenized'
	// }
}
