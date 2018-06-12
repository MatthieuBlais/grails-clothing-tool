import psycopg2
import sys

class DatabaseConnector(object):
	"""docstring for DatabaseConnector"""
	def __init__(self, connection_string="host='matthieu.c9ugkbttzgdh.ap-southeast-1.rds.amazonaws.com' dbname='meow' user='crawler' password='M4ch4tt3!'"):
		super(DatabaseConnector, self).__init__()
		#connection_string="host='localhost' dbname='meow' user='dashboard' password='3006Jollibee'"
		self.conn_string = connection_string
		self.con = psycopg2.connect(self.conn_string)
		self.cur = self.con.cursor()
		

	def commit(self):
		self.con.commit()

	def execute(self, query, fetch=False):
		self.cur.execute(query)
		if fetch:
			return self.cur.fetchall()

	def select(self, table, attributes, conditions):
		query="SELECT "+self.format_attributes(attributes)+" FROM "+table
		if len(conditions)>0:
			query+=" WHERE "+self.and_format_conditions(conditions)
		self.cur.execute(query)
		results = self.cur.fetchall()
		return results

	def insertOrSelect(self, table, attributes, values, conditions):
		results = self.select(table, attributes, conditions)
		if len(results) == 0:
			query = "INSERT INTO "+table+"("+self.format_attributes(attributes)+") VALUES ("+self.format_values(values)+")"
			self.cur.execute(query)
		return True

	def insert(self, table, attributes, values):
		query = "INSERT INTO "+table+"("+self.format_attributes(attributes)+") VALUES ("+self.format_values(values)+")"
		self.cur.execute(query)
		return True

	def update(self, table, values, conditions=[]):
		query="UPDATE "+table+" SET "+self.format_update_values(values)
		if len(conditions) !=0:
			query+= " WHERE "+self.and_format_conditions(conditions)
		self.cur.execute(query)
		return True

	def insertOrUpdate(self, table, attributes, values, conditions):
		query = ""

	def delete(self, table, conditions):
		query= "DELETE FROM "+table
		if len(conditions)>0:
			query += " WHERE "+self.and_format_conditions(conditions)
		self.cur.execute(query)

	def select_next_id(self, table):
		query="SELECT MAX(id) FROM "+table 
		self.cur.execute(query)
		results = self.cur.fetchone()
		if results[0] == None:
			return 1
		else:
			return results[0]+1

	def format_attributes(self, attributes):
		return ", ".join(attributes)

	def format_values(self, values):
		s = []
		for val in values:
			if val[0] == None:
				val[1] = "NULL"
				val[0] = "null"
			if val[1] == "String":
				val[0] = "\'"+str(val[0].encode("utf8")).replace("\xc9", "").replace("\xc2","").replace('\xa0', '').replace("\xae","").replace("'", "''")+"\'"
			if val[1] == "Date":
				val[0] = "\'"+str(val[0])+"\'"
			if val[1] == "Boolean":
				if val[0]:
					val[0] = "true"
				else:
					val[0] = "false"
			val[0] = str(val[0])
			s.append(val[0])
		return ", ".join(s)

	def format_update_values(self, values):
		s = []
		for val in values:
			if val[1] == None:
				val[2] = "NULL"
				val[1] = "null"
			if val[2] == "String" :
				val[1] = "\'"+str(val[1].encode("utf8")).replace("\xc2","").replace('\xa0', '').replace("\xae","").replace("\xc9", "").replace("'", "''")+"\'"
			if val[2] == "Date":
				val[1] = "\'"+str(val[1])+"\'"
			if val[2] == "Boolean":
				if val[1]:
					val[1] = "true"
				else:
					val[1] = "false"
			val[1] = str(val[1])
			s.append(val[0]+"="+val[1])
		return ", ".join(s)

	def and_format_conditions(self, conditions):
		s = []
		for cond in conditions:
			if cond[2] == None:
				cond[3] = "NULL"
				if cond[1]=="=":
					cond[1]="is"
			if cond[3] == "String":
				#print cond[2]
				cond[2] = "\'"+str(cond[2].encode("utf8").replace("\xc9", "").replace("\xc2","").replace('\xa0', '').replace("\xae","").replace("'", "''"))+"\'"
			if cond[3] == "Date":
				cond[2] = "\'"+str(cond[2]).replace("\xc9", "").replace("\xc2","").replace('\xa0', '').replace("\xae","").replace("'", "''")+"\'"
			if cond[3] == "Boolean":
				if cond[2]:
					cond[2] = "true"
				else:
					cond[2] = "false"
			cond[2] = str(cond[2])
			cond = cond[:3]
			s.append(" ".join(cond))
		return " and ".join(s)

	def or_format_conditions(self, conditions):
		s = []
		for cond in conditions:
			if cond[3] == "String" or cond[3] == "Date":
				cond[2] = "\'"+str(cond[2]).replace("\xc2","").replace('\xa0', '').replace("\xae","").replace("\xc9", "").replace("'", "''")+"\'"
			cond[2] = str(cond[2])
			cond = cond[:3]
			s.append(" ".join(cond))
		return " or ".join(s)

	def format_many_values(self, data):
		output = []
		for values in data:
			s = []
			#print values
			for val in values:
				if val[0] == None:
					val[1] = "NULL"
					val[0] = None
				if val[1] == "String":
					if len(val[0])>0:
						if val[0][0] == "'" and val[0][len(val)-1]=="'":
							val[0] = val[1:len(val)-1]
							val[0] = str(val[0]).replace("\xc2","").replace('\xa0', '').replace("\xae","").replace("\xc9", "")
					else:
						val[0] = None
				if val[1] == "Date":
					val[0] = val[0]
				if val[1] == "Boolean":
					if val[0]:
						val[0] = True
					else:
						val[0] = False
				if val[1] == "Int" or val[1]=="Float":
					if isinstance(val[0], basestring):
						if "," in val[0] and "." in val[0]:
							val[0] = val[0].replace(",","")
				s.append(val[0])
			output.append(tuple(s))
		return output

	def execute_many_inserts(self, table, attributes, data):
		#print "INSERT INTO "+table+" ("+self.format_attributes(attributes)+") VALUES ("+",".join(["%s" for x in range(len(attributes))])+")", self.format_many_values(data)
		#sys.exit()
		self.cur.executemany("INSERT INTO "+table+" ("+self.format_attributes(attributes)+") VALUES ("+",".join(["%s" for x in range(len(attributes))])+")", self.format_many_values(data))

	def execute_many_updates(self, table, attributes, conditions, data):
		self.cur.executemany("UPDATE "+table+" SET "+",".join([x+"=%s" for x in attributes])+" WHERE "+",".join([x[0]+x[1]+" %s" for x in conditions]), self.format_many_values(data))

	def execute_many_deletes(self, table, conditions, data):
		self.cur.executemany("DELETE FROM "+table+" WHERE "+",".join([x[0]+x[1]+" %s" for x in conditions]), self.format_many_values(data))