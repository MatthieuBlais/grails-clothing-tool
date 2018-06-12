import uuid

from DatabaseConnector import DatabaseConnector as db

class Websites(object):
	"""docstring for Websites"""
	def __init__(self, db_connector):
		super(Websites, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "name", "url"]
		self.attribute_definition = {
			"id": "String",
			"version": "Int",
			"name": "String",
			"url":"String"
		}

	def save(self, name, url=None):
		website_id = uuid.uuid1().hex
		self.db.insert("websites", self.attributes, [[website_id, "String"], [0, "Int"], [name, "String"], [url, "String"]])
		#self.db.commit()
		results = self.db.select("websites", self.attributes, [["id", "=", website_id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "url": results[0][3]}

	def delete(self, website_id):
		self.db.delete("websites", [["id", "=", website_id, "String"]])
		#self.db.commit()
		return True

	def find_by_name(self, name):
		results = self.db.select("websites", self.attributes, [["name", "=", name, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "url": results[0][3]}

	def find_by_id(self, id):
		results = self.db.select("websites", self.attributes, [["id", "=", id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "name": results[0][2], "url": results[0][3]}


# db = db()

# website = Websites(db)

# website.save("dressabelle", "https://www.dressabelle.com.sg/")



# print website.findByName("dressabelle")