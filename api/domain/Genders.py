from DatabaseConnector import DatabaseConnector as db


class Genders(object):
	"""docstring for Genders"""
	def __init__(self, db_connector):
		super(Genders, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "name"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"name": "String"
		}

	def save(self, name):
		gender_id = self.db.select_next_id("genders")
		self.db.insert("genders", self.attributes, [[gender_id, "Int"], [0, "Int"], [name.title(), "String"]])
		#self.db.commit()
		results = self.db.select("genders", self.attributes, [["id", "=", gender_id, "Int"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2]}

	def delete(self, gender_id):
		self.db.delete("genders", [["id", "=", gender_id, "String"]])
		#self.db.commit()
		return True

	def find_by_name(self, name):
		results = self.db.select("genders", self.attributes, [["name", "=", name.title(), "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2]}

	def find_by_id(self, id):
		results = self.db.select("genders", self.attributes, [["id", "=", id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2]}

	def find_all(self):
		genders = self.db.execute("SELECT id, name from genders", fetch=True)
		return { x[1]: {"id": x[0], "name": x[1]} for x in genders }





		