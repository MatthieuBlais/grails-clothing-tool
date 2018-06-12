from DatabaseConnector import DatabaseConnector as db


class Brands(object):
	"""docstring for Brands"""
	def __init__(self, db_connector):
		super(Brands, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "name", "type"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"name": "String",
			"type": "String"
		}

	def save(self, name, type=None):
		brand_id = self.db.select_next_id("brands")
		self.db.insert("brands", self.attributes, [[brand_id, "Int"], [0, "Int"], [name, "String"], [type, "String"]])
		#self.db.commit()
		results = self.db.select("brands", self.attributes, [["id", "=", brand_id, "Int"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def delete(self, brand_id):
		self.db.delete("brands", [["id", "=", brand_id, "String"]])
		#self.db.commit()
		return True

	def find_by_name(self, name):
		results = self.db.select("brands", self.attributes, [["name", "=", name, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def find_by_id(self, id):
		results = self.db.select("brands", self.attributes, [["id", "=", id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def find_all(self):
		brands = self.db.execute("SELECT id, name from brands", fetch=True)
		return { x[1]: {"id": x[0], "name": x[1]} for x in brands }
