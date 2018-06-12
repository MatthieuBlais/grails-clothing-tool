import uuid

from DatabaseConnector import DatabaseConnector as db


class Variants(object):
	"""docstring for Sizes"""
	def __init__(self, db_connector):
		super(Variants, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "variant_id", "product_id", "size", "color"]
		self.attribute_definition = {
			"id": "Int",
			"version": "Int",
			"variant_id": "String",
			"product_id": "String",
			"size":"String",
			"color": "String"
		}


	def save(self, variant, prod_id, size=None, color=None):
		variant_id = self.db.select_next_id("variants")
		if size:
			size = size.upper()
		if color:
			color = color.title()
		self.db.insert("variants", self.attributes, [[variant_id, "Int"], [0, "Int"], [variant, "String"], [prod_id, "String"], [size, "String"], [color, "String"]])
		return {"id": variant_id, "variant_id": variant, "size": size, "color":color, "product_id":prod_id}

	def delete(self, variant_id):
		self.db.delete("variants", [["id", "=", variant_id, "Int"]])
		#self.db.commit()
		return True

	def find_by_variant(self, variant):
		results = self.db.select("variants", self.attributes, [["variant_id", "=", str(variant), "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "variant_id": variant, "product_id": results[0][3], "size": results[0][4], "color": results[0][5]}

	def find_all(self, grouped=True):
		variants = self.db.execute("SELECT id, variant_id, size, color, product_id from variants", fetch=True)
		all_variants = { x[1]: {"id": x[0], "variant": x[1], "size":x[2], "color":x[3], "product_id": x[4]} for x in variants }
		if grouped:
			output = {}
			for k in all_variants.keys():
				if all_variants[k]["product_id"] not in output.keys():
					output[all_variants[k]["product_id"]] = {}
				output[all_variants[k]["product_id"]][k] = all_variants[k]
			return output
		return all_variants





# db = db()

# size = Sizes(db)

# size.save("xs", "test")



# print size.findByName("xs")