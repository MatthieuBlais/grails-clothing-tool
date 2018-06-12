import uuid

from DatabaseConnector import DatabaseConnector as db
from Styles import Styles
import time

class ProductStyles(object):
	"""docstring for ProductStyles"""
	def __init__(self, db_connector):
		super(ProductStyles, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "style_id", "product_id", "is_generated"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"style_id": "Int",
			"product_id":"String",
			"is_generated":"Boolean"
		}

	def save(self,product, style, is_generated=False):
		product_style_id = self.db.select_next_id("product_styles")
		self.db.insert("product_styles", self.attributes, [[product_style_id, "Int"], [0, "Int"], [style["id"], "Int"], [product["id"], "String"], [is_generated, "Boolean"]])
		#self.db.commit()
		results = self.db.select("product_styles", self.attributes, [["id", "=", product_style_id, "Int"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "is_generated": results[0][4], "style": style, "product":product}

	def insert_query(self,product, style, is_generated=False):
		product_style_id = uuid.uuid1().hex
		return [[product_style_id, "Int"], [0, "Int"], [style["id"], "Int"], [product["id"], "String"], [is_generated, "Boolean"]]

	def delete(self, ps_id):
		self.db.delete("product_styles", [["id", "=", ps_id, "String"]])
		#self.db.commit()
		return True

	def find_all_by_product(self, product, inclusive=False, existing_styles = {}):
		results = self.db.select("product_styles", self.attributes, [["product_id", "=", product["id"], "String"]])
		output = []
		existing={}
		Style = Styles(self.db)
		if len(existing_styles.keys())>0:
			existing = { existing_styles[k]["id"] : existing_styles[k] for k in existing_styles }
		for r in results:
			if r[2] in existing.keys():
				style = existing[r[2]]
			else:
				style = Style.find_by_id(r[2])
			if style:
				if inclusive:
					output.append({"id": r[0], "is_generated": r[4], "style": style, "product":product})
				else:
					output.append({"id": r[0], "is_generated": r[4], "style": style})
		return output

	def delete_missing_styles(self, product, style_labels, product_styles, query=False):
		styles_labels = [x.title() for x in style_labels]
		current_style_labels = [ps["style"]["name"] for ps in product_styles if ps["is_generated"]== False]
		ps_lookup = { ps["style"]["name"]: ps["id"] for ps in product_styles if ps["is_generated"]== False}
		deleted_styles = [x for x in current_style_labels if x not in styles_labels]
		delete_queries = []
		for style in deleted_styles:
			ps_id = ps_lookup[style]
			if not query:
				self.delete(ps_id)
			else:
				delete_queries.append([[ps_id, "String"]])
		return delete_queries

	def insert_many(self, data):
		if len(data)>0:
			self.db.execute_many_inserts("product_styles", self.attributes, data)

	def delete_many(self, data):
		if len(data)>0:
			self.db.execute_many_deletes("product_styles", [["id", "="]], data)