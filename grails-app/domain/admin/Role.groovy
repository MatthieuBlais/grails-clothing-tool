package db

import grails.gorm.DetachedCriteria
import groovy.transform.EqualsAndHashCode
import groovy.transform.ToString
import grails.compiler.GrailsCompileStatic

@GrailsCompileStatic
@EqualsAndHashCode(includes='authority')
@ToString(includes='authority', includeNames=true, includePackage=false)
class Role implements Serializable {

	private static final long serialVersionUID = 1

	String id
	String authority
	int		priority
	String description

	static boolean exists(String _authority) {
		criteriaFor(_authority).count()
	}

	private static DetachedCriteria criteriaFor(String _authority) {
		Role.where {
			authority == _authority
		}
	}

	static constraints = {
		id 			maxSize:32, column:'id'
		authority blank: false, unique: true
		priority nullable:true
		description nullable:true
	}

	static mapping = {
		id generator:'uuid'
		authority index:'role_id'
		cache true
	}
}
