import uuid

from DatabaseConnector import DatabaseConnector as db
import datetime
import uuid



class Prices(object):
	"""docstring for Prices"""
	def __init__(self, db_connector):
		super(Prices, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "create_at", "currency", "product_id", "value", "is_discount"]
		self.attribute_definition = {
			"id": "String",
			"version": "Int",
			"create_at": "Date",
			"currency": "String",
			"product_id":"String",
			"value": "Float",
			"is_discount":"Boolean"
		}

	def save(self, product, value, currency="SG$", create_at=datetime.datetime.now(), is_discount = False):
		price_id = uuid.uuid1().hex
		self.db.insert("prices", self.attributes, [[price_id, "String"], [0, "Int"], [create_at, "Date"], [currency, "String"], [product["id"], "String"], [value, "Float"], [is_discount, "Boolean"]])
		#self.db.commit()
		results = self.db.select("prices", self.attributes, [["id", "=", price_id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "create_at": results[0][2], "currency": results[0][3], "product":product, "value":results[0][5], "is_discount":results[0][6]}

	def insert_query(self, product, value, currency="SG$", create_at=datetime.datetime.now(), is_discount = False):
		price_id = uuid.uuid1().hex
		return [[price_id, "String"], [0, "Int"], [create_at, "Date"], [currency, "String"], [product["id"], "String"], [value, "Float"], [is_discount, "Boolean"]]

	def delete(self, price_id):
		self.db.delete("prices", [["id", "=", price_id, "String"]])
		#self.db.commit()
		return True

	def find_all_by_product(self, product):
		results = self.db.select("prices", self.attributes, [["product_id", "=", product["id"], "String"]])
		output = []
		Size = Sizes(self.db)
		for r in results:
			size = Size.find_by_id(r[3])
			if size:
				output.append({"id": results[0][0], "create_at": results[0][2], "currency": results[0][3], "product":product, "value":results[0][5], "is_discount":results[0][6]})
		return output

	def find_by_id(self, id):
		results = self.db.select("prices", self.attributes, [["id", "=", id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "create_at": results[0][2], "currency": results[0][3], "product_id":results[0][4], "value":results[0][5], "is_discount":results[0][6]}

	def insert_many(self, data):
		if len(data)>0:
			self.db.execute_many_inserts("prices", self.attributes, data)