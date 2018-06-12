import uuid

from DatabaseConnector import DatabaseConnector as db


class Sizes(object):
	"""docstring for Sizes"""
	def __init__(self, db_connector):
		super(Sizes, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "name", "type"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"name": "String",
			"type":"String"
		}


	def save(self, name, type=None):
		size_id = uuid.uuid1().hex
		self.db.insert("sizes", self.attributes, [[size_id, "String"], [0, "Int"], [name.upper(), "String"], [type, "String"]])
		#self.db.commit()
		results = self.db.select("sizes", self.attributes, [["id", "=", size_id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def delete(self, website_id):
		self.db.delete("sizes", [["id", "=", website_id, "String"]])
		#self.db.commit()
		return True

	def find_by_name(self, name):
		results = self.db.select("sizes", self.attributes, [["name", "=", name.upper(), "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def find_by_id(self, _id):
		results = self.db.select("sizes", self.attributes, [["id", "=", _id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "type": results[0][3]}

	def find_all(self):
		sizes = self.db.execute("SELECT id, name from sizes", fetch=True)
		return { x[1]: {"id": x[0], "name": x[1]} for x in sizes }





# db = db()

# size = Sizes(db)

# size.save("xs", "test")



# print size.findByName("xs")