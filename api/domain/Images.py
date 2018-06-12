import uuid

from DatabaseConnector import DatabaseConnector as db




class Images(object):
	"""docstring for Images"""
	def __init__(self, db_connector):
		super(Images, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "cloud_storage", "local_storage", "is_main_picture", "product_id", "url"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"cloud_storage": "String",
			"local_storage": "String",
			"is_main_picture": "Boolean",
			"product_id":"String",
			"url": "String"
		}


	def save(self, url, product, cloud_storage=None, is_main_picture=False, local_storage=None):
		image_id = uuid.uuid1().hex
		self.db.insert("images", self.attributes, [[image_id, "String"], [0, "Int"], [cloud_storage, "String"], [local_storage,"String"], [is_main_picture, "Boolean"], [product["id"], "String"], [url, "String"]])
		#self.db.commit()
		results = self.db.select("images", self.attributes, [["id", "=", image_id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "cloud_storage": results[0][2], "local_storage": results[0][3], "is_main_picture": results[0][4], "product": product, "url": results[0][6]}

	def insert_query(self, url, product, cloud_storage=None, is_main_picture=False, local_storage=None):
		image_id = uuid.uuid1().hex
		return [[image_id, "String"], [0, "Int"], [cloud_storage, "String"], [local_storage,"String"], [is_main_picture, "Boolean"], [product["id"], "String"], [url, "String"]]

	def delete(self, image_id):
		self.db.delete("images", [["id", "=", image_id, "String"]])
		#self.db.commit()
		return True

	def find_by_url(self, url):
		results = self.db.select("images", self.attributes, [["url", "=", url, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "cloud_storage": results[0][2], "local_storage": results[0][3], "is_main_picture": results[0][4], "product": product, "url": results[0][6]}

	def find_by_id(self, _id):
		results = self.db.select("images", self.attributes, [["id", "=", _id, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "cloud_storage": results[0][2], "local_storage": results[0][3], "is_main_picture": results[0][4], "product": product, "url": results[0][6]}

	def find_all_by_product(self, product):
		results = self.db.select("images", self.attributes, [["product_id", "=", product["id"], "String"]])
		output = []
		for r in results:
			output.append({"id": r[0], "cloud_storage": r[2], "local_storage": r[3], "is_main_picture": r[4], "product": product, "url": r[6]})
		return output

	def get_main_picture(self, product):
		results = self.db.select("images", self.attributes, [["product_id", "=", product["id"], "String"], ["is_main_picture", "=", True, "Boolean"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "cloud_storage": results[0][2], "local_storage": results[0][3], "is_main_picture": results[0][4], "product": product, "url": results[0][6]}

	def reset_main_picture(self, product):
		self.db.update("images", [["is_main_picture", False, "Boolean"]], [["product_id", "=", product["id"], "String"]])
		#self.db.commit()

	def update_main_picture(self, product, image=None, url=None):
		if image == None and url == None:
			return False 
		self.reset_main_picture(product)
		if image != None:
			self.db.update("images", [["is_main_picture", True, "Boolean"]], [["product_id", "=", product["id"], "String"], ["id", "=", image["id"], "String"]])
		else:
			self.db.update("images", [["is_main_picture", True, "Boolean"]], [["product_id", "=", product["id"], "String"], ["url", "=", url, "String"]])
		#self.db.commit()
		return True

	def delete_missing_pictures(self, product, urls, product_images, query=False):
		#product_images = self.find_all_by_product(product)
		current_images = [img["url"]for img in product_images]
		img_lookup = {img["url"]: img["id"] for img in product_images}
		deleted_img = [x for x in current_images if x not in urls]
		delete_queries = []
		for img in deleted_img:
			img_id = img_lookup[img]
			if not query:
				self.delete(img_id)
			else:
				delete_queries.append([[img_id, "String"]])
		return delete_queries

	def insert_many(self, data):
		if len(data)>0:
			self.db.execute_many_inserts("images", self.attributes, data)

	def delete_many(self, data):
		if len(data)>0:
			self.db.execute_many_deletes("images", [["id", "="]], data)