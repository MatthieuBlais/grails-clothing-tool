from DatabaseConnector import DatabaseConnector as db


class Styles(object):
	"""docstring for Styles"""
	def __init__(self, db_connector):
		super(Styles, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "name", "type"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int", 
			"name": "String",
			"type":"String",
			
		}

	def save(self, name, type=None):
		style_id = self.db.select_next_id("styles")
		self.db.insert("styles", self.attributes, [[style_id, "Int"], [0, "Int"], [name.title(), "String"], [type, "String"]])
		#self.db.commit()
		results = self.db.select("styles", self.attributes, [["id", "=", style_id, "Int"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def delete(self, style_id):
		self.db.delete("styles", [["id", "=", style_id, "String"]])
		#self.db.commit()
		return True

	def find_by_name(self, name):
		results = self.db.select("styles", self.attributes, [["name", "=", name.title(), "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def find_by_id(self, id):
		results = self.db.select("styles", self.attributes, [["id", "=", id, "Int"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def find_all(self):
		styles = self.db.execute("SELECT id, name from styles", fetch=True)
		return { x[1]: {"id": x[0], "name": x[1]} for x in styles }
