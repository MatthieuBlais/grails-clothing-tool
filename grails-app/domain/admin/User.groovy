package db

import groovy.transform.EqualsAndHashCode
import groovy.transform.ToString

@EqualsAndHashCode(includes='email')
@ToString(includes='firstname', includeNames=true, includePackage=false)
class User implements Serializable {


	private static final long serialVersionUID = 1
	
	def springSecurityService
	static transients = ['springSecurityService', 'passwordConfirm']


	String id
	String firstname
	String lastname
	String profilePicture
	String email 
	
	String password
	String username

	Date	createAt
	Date	updateAt
	String	createBy
	String	updateBy

	Boolean enabled = true
	Boolean passwordExpired
	Boolean accountExpired
	Boolean accountLocked

	String resetPasswordToken
	Date resetPasswordDate


	Set<Role> getAuthorities() {
		// def groups = (UserGroup.findAllByUser(this) as List<UserGroup>)*.getAuthorities() as Set<Role>
		// groups.addAll((UserRole.findAllByUser(this) as List<UserRole>)*.role  as Set<Role>)
		// return groups
		(UserRole.findAllByUser(this) as List<UserRole>)*.role  as Set<Role>
	}

	Boolean hasAuthority(String authority){
		def role =  Role.findByAuthority(authority)
		return UserRole.countByUserAndRole(this,role)
	}

	def beforeInsert() {
		//encodePassword()
		accountExpired = false
		accountLocked = false
		createAt = new Date()
		updateAt = new Date()
		// createBy = springSecurityService.getCurrentUser().id
		// updateBy = springSecurityService.getCurrentUser().id
		firstname = firstname != null ? firstname.substring(0, 1).toUpperCase() + firstname.substring(1).toLowerCase() : firstname
		lastname = lastname != null ? lastname.substring(0, 1).toUpperCase() + lastname.substring(1).toLowerCase() : lastname
	}

	def beforeUpdate() {
		updateAt = new Date()
		updateBy = springSecurityService?.getCurrentUser()? springSecurityService?.getCurrentUser().id : "system"
		firstname = firstname != null ? firstname.substring(0, 1).toUpperCase() + firstname.substring(1).toLowerCase() : firstname
		lastname = lastname != null ? lastname.substring(0, 1).toUpperCase() + lastname.substring(1).toLowerCase() : lastname
		if (isDirty('password')) {
			encodePassword()
		}
	}

	def updatePassword(pswd){
		password=pswd
	}

	protected void encodePassword() {
		password = springSecurityService.encodePassword(password)
	}


    static constraints = {
    	id 	maxSize: 32, column: 'id'
		firstname maxSize:64, nullable:false, blank:false
		lastname maxSize:64, nullable:false, blank:false
		profilePicture maxSize:2083, nullable:true
		email blank: false, unique: true, maxSize:32, nullable:true
		
		resetPasswordToken nullable: true
		resetPasswordDate nullable: true
		accountExpired nullable:true
		accountLocked nullable:true

		password blank: false, password: true
		username blank: false, unique: true

		createAt nullable:true
    	updateAt nullable:true
    	createBy nullable:true
    	updateBy nullable:true
    }

    static mapping = {
		table 'tuser'
		password column: '`password`'
		id	generator:'uuid'
		cache true
	}

	public String fullName(){
		return firstname.substring(0, 1).toUpperCase() + firstname.substring(1).toLowerCase()+" "+lastname.substring(0, 1).toUpperCase() + lastname.substring(1).toLowerCase()
	}

	public String shortName(){
		return firstname.substring(0, 1).toUpperCase() + firstname.substring(1).toLowerCase()
	}

	public String getProfilePicture(){
		return profilePicture != null && !profilePicture.isEmpty() ? profilePicture : '/assets/default-profile.png'
	}
}
