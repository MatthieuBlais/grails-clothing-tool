import uuid

from DatabaseConnector import DatabaseConnector as db
from Sizes import Sizes



class ProductSizes(object):
	"""docstring for ProductSizes"""
	def __init__(self, db_connector):
		super(ProductSizes, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "available", "size_id", "product_id"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"available": "Boolean",
			"size_id": "String",
			"product_id":"String"
		}

	def save(self,product, size, available=True):
		product_size_id = uuid.uuid1().hex
		self.db.insert("product_sizes", self.attributes, [[product_size_id, "String"], [0, "Int"], [available, "Boolean"], [size["id"], "String"], [product["id"], "String"]])
		#self.db.commit()
		results = self.db.select("product_sizes", self.attributes, [["id", "=", product_size_id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "available": results[0][2], "size": size, "product":product}

	def insert_query(self,product, size, available=True):
		product_size_id = uuid.uuid1().hex
		return [[product_size_id, "String"], [0, "Int"], [available, "Boolean"], [size["id"], "String"], [product["id"], "String"]]

	def delete(self, ps_id):
		self.db.delete("product_sizes", [["id", "=", ps_id, "String"]])
		#self.db.commit()
		return True

	def find_all_by_product(self, product, inclusive=False):
		results = self.db.select("product_sizes", self.attributes, [["product_id", "=", product["id"], "String"]])
		output = []
		Size = Sizes(self.db)
		for r in results:
			size = Size.find_by_id(r[3])
			if size:
				if inclusive:
					output.append({"id": r[0], "available": r[2], "size": size, "product":product})
				else:
					output.append({"id": r[0], "available": r[2], "size": size})
		return output

	def update_availability(self, ps_id, availability, query=False):
		if not query:
			self.db.update("product_sizes", [["available", availability, "Boolean"]], [["id", "=", ps_id, "String"]])
			#self.db.commit()
			return True
		else:
			return [[availability, "Boolean"], [ps_id, "String"]]

	def delete_missing_sizes(self, product, size_labels, product_sizes, mode="delete", query=False):
		#product_sizes = self.find_all_by_product(product)
		size_labels = [x.upper() for x in size_labels]
		current_size_labels = [ps["size"]["name"] for ps in product_sizes]
		ps_lookup = { ps["size"]["name"]: ps["id"] for ps in product_sizes}
		deleted_sizes = [x for x in current_size_labels if x not in size_labels]
		delete_queries = []
		for size in deleted_sizes:
			ps_id = ps_lookup[size]
			if not query:
				if mode == "delete":
					self.delete(ps_id)
				elif mode == "unavailable":
					self.update_availability(ps_id, False)
			else:
				delete_queries.append([[ps_id, "String"]])
		return delete_queries

	def update_many_availability(self, data):
		if len(data)>0:
			self.db.execute_many_updates("product_sizes", ["available"], [["id", "="]], data)

	def insert_many(self, data):
		if len(data)>0:
			self.db.execute_many_inserts("product_sizes", self.attributes, data)

	def delete_many(self, data):
		if len(data)>0:
			self.db.execute_many_deletes("product_sizes", [["id", "="]], data)

	def delete_previous(self, products, new_ids):
		if len(new_ids)>0 and len(products)>0:
			self.db.execute("DELETE FROM product_sizes where product_id in ("+",".join(["\'"+x+"\'" for x in products])+") and id not in ("+",".join(["\'"+x+"\'" for x in new_ids])+")")