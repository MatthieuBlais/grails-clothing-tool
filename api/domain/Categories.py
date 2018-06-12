from DatabaseConnector import DatabaseConnector as db


class Categories(object):
	"""docstring for Categories"""
	def __init__(self, db_connector):
		super(Categories, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "name", "label", "gender_id","category_id"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"name": "String",
			"label": "String",
			"gender_id":"Int",
			"category_id":"Int"
		}


	def save(self, name, label=None, gender=None, category=None):
		cat_id = self.db.select_next_id("categories")
		self.db.insert("categories", self.attributes, [[cat_id, "Int"], [0, "Int"], [name.title(), "String"], [label, "String"], [gender, "Int"], [category, "Int"]])
		#self.db.commit()
		results = self.db.select("categories", self.attributes, [["id", "=", cat_id, "Int"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "label": results[0][3], "gender":results[0][4], "category": results[0][5]}

	def delete(self, cat_id):
		self.db.delete("categories", [["id", "=", cat_id, "String"]])
		#self.db.commit()
		return True

	def find_by_name_and_gender(self, name, gender=None):
		results = self.db.select("categories", self.attributes, [["name", "=", name.title(), "String"], ["gender_id", "=", gender, "Int"]])
		if len(results) == 0:
			return None
		return {"id": results[0][0], "name": results[0][2], "label": results[0][3], "gender":results[0][4], "category": results[0][5]}

	def find_by_id(self, id):
		results = self.db.select("categories", self.attributes, [["id", "=", id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "label": results[0][3], "gender":results[0][4], "category": results[0][5]}

	def find_all(self):
		cats = self.db.execute("SELECT id, name from categories", fetch=True)
		return { x[1]: {"id": x[0], "name": x[1]} for x in cats }