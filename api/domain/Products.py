from DatabaseConnector import DatabaseConnector as db
from Categories import Categories
from Brands import Brands
from Websites import Websites
from ProductSizes import ProductSizes
from Images import Images
from Sizes import Sizes 
from Genders import Genders
from Prices import Prices
from Styles import Styles
from ProductStyles import ProductStyles
from Variants import Variants
import uuid
import datetime
import time

class Products(object):
	"""docstring for Products"""
	def __init__(self, db_connector):
		super(Products, self).__init__()
		self.db = db_connector
		self.attributes = ["id", "version", "category_id", "create_at", "name", "sku"]
		self.other_attributes = ["brand_id", "description", "subcategory_id", "url", "website_id" ]
		self.missing_attributes = ["current_discount_id", "current_price_id", "generated_description", "update_at"]
		self.forgotten_attributes = ["gender_id", "color"]
		self.additional_attributes = ["need_additional_data", "need_process"]
		self.attribute_definition = {
			"id": "String",
			"version": "Int",
			"brand_id": "String",
			"gender_id": "String",
			"category_id":"Int",
			"color":"String",
			"create_at":"Date",
			"current_discount_id": "String",
			"current_price_id": "String",
			"description":"String",
			"generated_description":"String",
			"name":"String",
			"sku":"String",
			"subcategory_id":"String",
			"update_at":"Date",
			"url":"String",
			"website_id":"String",
			"need_additional_data": "Boolean",
			"need_process": "Boolean"
		}


	def save_from_json(self, data):
		if data["category"] == None or data["sku"]==None or data["name"]==None or data["website_id"]==None:
			return None
		sku =  data["website_id"]+"-"+str(data["sku"])
		gender = self.get_or_create_gender_by_name(data["gender"])
		category = self.get_or_create_category_by_name(data["category"], gender=gender)
		brand = self.get_or_create_brand_by_name(data["brand"])
		description = "\n".join([x.strip() for x in data["features"] if len(x.strip())>0])
		if len([x.strip() for x in data["features"] if len(x.strip())>0]) ==0:
			description = None
		else:
			description = description.encode('utf-8')
		name = data["name"].strip().encode('utf-8')
		color = data["color"]
		if color:
			color = color.title()
		subcategory = None
		if "subcat" in data.keys():
			if data["subcat"] != None:
				subcategory = self.get_or_create_category_by_name(data["subcat"], gender=gender, parent=category)
				subcategory = subcategory["id"]
				category["id"] = subcategory["category"]
		url = data["url"]
		website = self.get_or_create_website_by_name(data["website_id"])
		style_line = self.update_style_line(data)


		product = self.find_by_sku(sku)
		if product:
			if description!=None:
				if product["description"] == None:
					description = description
				else:
					if len(product["description"])>0 and len(description)>0 and description!=product["description"]:
						description = description
					else:
						description = product["description"]
			else:
				description = product["description"] 
			self.db.update("products", [["update_at", datetime.datetime.now(), "Date"], ["description", description, "String"], ["color", color, "String"], ["style_line", style_line, "String"]], [["id", "=", product["id"], "String"]])
		else:
			create_at, update_at = self.get_create_date(data)
			product_id = uuid.uuid1().hex
			self.db.insert("products", self.attributes+self.other_attributes+self.forgotten_attributes+["update_at", "style_line"], [[product_id, "String"], [0, "Int"], [category["id"], "String"], [create_at, "Date"],[name, "String"],[sku, "String"],[brand["id"], "String"],[description, "String"], [subcategory, "String"], [url, "String"], [website["id"], "String"], [gender["id"], "Int"], [color, "String"], [update_at, "Date"], [style_line, "String"]])
			product = {"id":product_id, "current_price_id" :None, "current_discount_id":None}
		
		self.update_price(product, data['price'], data['discount'])
		self.add_sizes(product, data["size"])
		
		self.add_images(product, data["images"])
		self.add_styles(product, data)


		#self.db.commit()
		return self.select(product["id"])

	def update_description_1(self, sku, website_id, description):
		sku =  website_id+"-"+sku
		product = self.find_by_sku(sku)
		if product:
			self.db.update("products", [["description", description, "String"]], [["id", "=", product["id"], "String"]])
		return True

	def update_images(self, sku, website_id, images):
		sku =  website_id+"-"+sku
		product = self.find_by_sku(sku)
		if product:
			self.add_images(product, images)
		return True

	def update_sizes(self, sku, website_id, sizes):
		sku =  website_id+"-"+sku
		product = self.find_by_sku(sku)
		if product:
			self.add_sizes(product, sizes)
		return True


	def select(self, product_id):
		results = self.db.select("products", self.attributes+self.other_attributes+self.missing_attributes+self.forgotten_attributes, [["id", "=", product_id, "String"]])
		if len(results) != 1:
			return None
		product = {"id": results[0][0], "create_at": results[0][3], "name": results[0][4], "sku": results[0][5], "description": results[0][7], "url": results[0][9], "generated_description": results[0][13], "update_at": results[0][14], "color":results[0][16]}
		product["category"]=self.get_category_by_id(results[0][2])
		product["brand"]=self.get_brand_by_id(results[0][6])
		if results[0][8] != None:
			product["subcategory"]=self.get_category_by_id(results[0][8])
		else:
			product["subcategory"]=None
		product["website"] = self.get_website_by_id(results[0][10])
		product["gender"] = self.get_gender_by_id(results[0][15])
		if results[0][11] != None:
			product["current_discount"]=self.get_price_by_id(results[0][11])
		else:
			product["current_discount"]=None
		if results[0][12] != None:
			product["current_price"]=self.get_price_by_id(results[0][12])
		else:
			product["current_price"]=None
		product["sizes"]= self.get_sizes(product)
		product["images"]= self.get_images(product)
		product["styles"] = self.get_styles(product)
		return product



	def update_price(self, product, price, discount):
		current_price, current_discount = None, None
		if "current_price_id" in product.keys() and product["current_price_id"]!=None:
			current_price = self.get_price_by_id(product["current_price_id"])
		if "current_discount_id" in product.keys() and product["current_discount_id"]!=None:
			current_discount = self.get_price_by_id(product["current_discount_id"])

		end_promotion = False
		if current_discount != None and (len(discount)==0 or discount==None):
			end_promotion = True

		if len(discount)==0 or discount==None:
			self.db.update("products", [["current_discount_id", None, "String"]], [["id", '=', product["id"], "String"]])

		if len(price)>0:
			if end_promotion == True or current_price == None:
				price = self.add_price(product, price[0])
			if end_promotion == False and current_price != None:
				if current_price["value"] == float(price[0]["price"]) and current_price["currency"] == price[0]["currency"]:
					price = current_price
				else:
					price = self.add_price(product, price[0])
			if price:
				self.db.update("products", [["current_price_id", price["id"], "String"]], [["id", '=', product["id"], "String"]])

		if len(discount)>0:
			if current_discount != None:
				if current_discount["value"] == float(discount[0]["price"]) and current_discount["currency"] == discount[0]["currency"]:
					discount = current_discount
				else:
					discount = self.add_price(product, discount[0], is_discount=True)
			else:
				discount = self.add_price(product, discount[0], is_discount=True)
			if discount:
				self.db.update("products", [["current_discount_id", discount["id"], "String"]], [["id", '=', product["id"], "String"]])
		#self.db.commit()
		return True


	def add_price(self, product, price, is_discount=False):
		Price = Prices(self.db)
		create_at = datetime.datetime.now()
		if "start_date" in price:
			create_at = datetime.datetime.strptime(price["start_date"], '%y-%m-%d %H:%M')
		return Price.save(product, price["price"], currency=price["currency"], create_at=create_at, is_discount = is_discount)

	def add_price_2(self, product, price, is_discount=False):
		Price = Prices(self.db)
		create_at = datetime.datetime.now()
		if "start_date" in price:
			create_at = datetime.datetime.strptime(price["start_date"], '%y-%m-%d %H:%M')
		return Price.insert_query(product, price["price"], currency=price["currency"], create_at=create_at, is_discount = is_discount)

	def get_create_date(self, data):
		create_at = data["last_update"]
		if "zalora_catalog_upload_date" in data.keys():
			create_at = datetime.datetime.strptime(data["zalora_catalog_upload_date"], '%Y-%m-%d %H:%M:%S').strftime('%y-%m-%d %H:%M')
		return datetime.datetime.strptime(create_at, '%y-%m-%d %H:%M'), datetime.datetime.strptime(data["last_update"], '%y-%m-%d %H:%M')

	def get_or_create_category_by_name(self, cat_name, gender=None, parent=None):
		if cat_name == None:
			return None
		if gender != None:
			gender = gender["id"]
		if parent != None:
			parent = parent["id"]
		Category = Categories(self.db)
		category = Category.find_by_name_and_gender(cat_name.strip(), gender)
		if not category:
			category = Category.save(cat_name.strip(), gender=gender, category=parent)
		if not category:
			return None
		return category

	def get_or_create_gender_by_name(self, gender_name):
		if gender_name == None:
			return None
		Gender = Genders(self.db)
		gender = Gender.find_by_name(gender_name.strip())
		if not gender:
			gender = Gender.save(gender_name.strip())
		if not gender:
			return None
		return gender

	def get_or_create_brand_by_name(self, brand_name):
		if brand_name == None:
			return None
		Brand = Brands(self.db)
		brand = Brand.find_by_name(brand_name.strip())
		if not brand:
			brand = Brand.save(brand_name.strip())
		if not brand:
			return None
		return brand

	def get_or_create_website_by_name(self, website_name):
		if website_name == None:
			return None
		Website = Websites(self.db)
		website = Website.find_by_name(website_name.strip())
		if not website:
			website = Website.save(website_name.strip())
		if not website:
			return None
		return website

	def get_category_by_id(self, cat_id):
		if cat_id == None:
			return None
		Category = Categories(self.db)
		category = Category.find_by_id(cat_id)
		if not category:
			return None
		return category

	def get_gender_by_id(self, gen_id):
		if gen_id == None:
			return None
		Gender = Genders(self.db)
		gender = Gender.find_by_id(gen_id)
		if not gender:
			return None
		return gender

	def get_brand_by_id(self, brand_id):
		if brand_id == None:
			return None
		Brand = Brands(self.db)
		brand = Brand.find_by_id(brand_id)
		if not brand:
			return None
		return brand

	def get_website_by_id(self, website_id):
		if website_id == None:
			return None
		Website = Websites(self.db)
		website = Website.find_by_id(website_id.strip())
		if not website:
			return None
		return website

	def get_price_by_id(self, price_id):
		if price_id == None:
			return None
		Price = Prices(self.db)
		price = Price.find_by_id(price_id)
		if not price:
			return None
		return price

	def get_sizes(self, product):
		if product["id"] == None:
			return None
		ProductSize = ProductSizes(self.db)
		return ProductSize.find_all_by_product(product)

	def get_images(self, product):
		if product["id"] == None:
			return None
		Image = Images(self.db)
		return Image.find_all_by_product(product)

	def get_styles(self, product):
		if product["id"] == None:
			return None
		ProductStyle = ProductStyles(self.db)
		return ProductStyle.find_all_by_product(product)

	def add_sizes(self, product, sizes, existing_sizes={}):
		if sizes == None:
			return
		ProductSize = ProductSizes(self.db)
		Size = Sizes(self.db)
		current_sizes = ProductSize.find_all_by_product(product)
		current_sizes_labels = { x["size"]["name"]:x["id"] for x in current_sizes }
		for size in sizes:
			s = None
			if size["value"] in existing_sizes.keys():
				s = existing_sizes[size["value"]]
			else:
				s = Size.save(size["value"])
				existing_sizes[s["name"]] = s
			if "available" not in size.keys() and "status" in size.keys(): ## TO REMOVE
				size["available"] = True								   ## 
			if size["value"].upper() in current_sizes_labels.keys():
				ProductSize.update_availability(current_sizes_labels[size["value"].upper()], size["available"])
			else:
				ProductSize.save(product, s, size["available"])
		ProductSize.delete_missing_sizes(product, [x["value"] for x in sizes], mode="delete")
		return existing_sizes

	def add_sizes_2(self, product, sizes, existing_sizes={}):
		if sizes == None:
			return existing_sizes, [], [], []
		ProductSize = ProductSizes(self.db)
		Size = Sizes(self.db)
		current_sizes = ProductSize.find_all_by_product(product)
		current_sizes_labels = { x["size"]["name"]:x["id"] for x in current_sizes }
		update_availability_queries = []
		insert_product_sizes = []
		for size in sizes:
			s = None
			if size["value"] in existing_sizes.keys():
				s = existing_sizes[size["value"]]
			else:
				s = Size.save(size["value"])
				existing_sizes[s["name"]] = s
			if "available" not in size.keys() and "status" in size.keys(): ## TO REMOVE
				size["available"] = True								   ## 
			if size["value"].upper() in current_sizes_labels.keys():
				update_availability_queries.append(ProductSize.update_availability(current_sizes_labels[size["value"].upper()], size["available"], query=True))
			else:
				insert_product_sizes.append(ProductSize.insert_query(product, s, size["available"]))
		delete_missing_sizes_queries = ProductSize.delete_missing_sizes(product, [x["value"] for x in sizes], current_sizes, mode="delete", query=True)
		return existing_sizes, update_availability_queries, insert_product_sizes, delete_missing_sizes_queries

	def add_sizes_3(self, product, sizes, existing_sizes={}, existing_variants={}):
		if sizes == None:
			return existing_sizes, [], False
		ProductSize = ProductSizes(self.db)
		Size = Sizes(self.db)
		Variant = Variants(self.db)
		insert_product_sizes = []
		need_find_variant = False
		for size in sizes:
			s = None
			value = None
			if size["value"]!=None:
				value = size["value"].strip().upper().replace(" IN", "").replace("SIZE ", "")
			else:
				return existing_sizes, [], True
				if "variant" in size.keys():
					if str(size["variant"]) in existing_variants.keys():
						value = existing_variants[str(size["variant"])]["size"]
					else:
						need_find_variant = True
						return existing_sizes, [], True
			if value in existing_sizes.keys():
				s = existing_sizes[value]
			else:
				s = Size.save(value)
				existing_sizes[s["name"]] = s
			if "available" not in size.keys() and "status" in size.keys(): ## TO REMOVE
				size["available"] = True
			insert_product_sizes.append(ProductSize.insert_query(product, s, size["available"]))
		return existing_sizes, insert_product_sizes, need_find_variant

	def add_images(self, product, images):
		Image = Images(self.db)
		current_images = Image.find_all_by_product(product)
		current_images_urls = [ x["url"]for x in current_images ]
		for img in images:
			if img not in current_images_urls:
				Image.save(img, product)
		Image.delete_missing_pictures(product, images)

	def add_images_2(self, product, images):
		Image = Images(self.db)
		current_images = Image.find_all_by_product(product)
		current_images_urls = [ x["url"]for x in current_images ]
		insert_queries = []
		for img in images:
			if img not in current_images_urls:
			#if img not in current_images_urls:
				insert_queries.append(Image.insert_query(img, product))
		delete_queries = Image.delete_missing_pictures(product, images, current_images, query=True)
		return insert_queries, delete_queries

	def add_images_3(self, product, images):
		Image = Images(self.db)
		insert_queries = []
		for img in images:
			#if img not in current_images_urls:
				insert_queries.append(Image.insert_query(img, product))
		#delete_queries = Image.delete_missing_pictures(product, images, current_images, query=True)
		return insert_queries


	def add_styles(self, product, data, existing_styles={}):
		if "zalora_subcats" not in data.keys():
			return
		styles = data["zalora_subcats"]

		ProductStyle = ProductStyles(self.db)
		Style = Styles(self.db)
		current_styles = ProductStyle.find_all_by_product(product)
		current_styles_labels = { x["style"]["name"]:x["id"] for x in current_styles }
		for style in styles:
			s = None
			if style in existing_styles.keys():
				s = existing_styles[style]
			else:
				s = Style.save(style)
				existing_styles[s["name"]] = s
			ProductStyle.save(product, s, False)
		ProductStyle.delete_missing_styles(product, [x for x in styles])
		return existing_styles

	def add_styles_2(self, product, data, existing_styles={}):
		if "zalora_subcats" not in data.keys():
			return existing_styles, [], [], None
		styles = data["zalora_subcats"]

		ProductStyle = ProductStyles(self.db)
		Style = Styles(self.db)
		current_styles = ProductStyle.find_all_by_product(product, existing_styles=existing_styles)
		current_styles_labels = { x["style"]["name"]:x["id"] for x in current_styles }
		insert_queries = []
		delete_queries = []
		for style in styles:
			s = None
			if style in existing_styles.keys():
				s = existing_styles[style]
			else:
				s = Style.save(style)
				existing_styles[s["name"]] = s
			insert_queries.append(ProductStyle.insert_query(product, s, False))
		
		start = time.time()
		delete_queries = ProductStyle.delete_missing_styles(product, [x for x in styles], current_styles, query=True)
		end = time.time() - start
		return existing_styles, insert_queries, delete_queries, end

	def add_styles_3(self, product, data, existing_styles={}):
		if "zalora_subcats" not in data.keys():
			return existing_styles, []
		styles = data["zalora_subcats"]
		ProductStyle = ProductStyles(self.db)
		Style = Styles(self.db)
		insert_queries = []
		for style in styles:
			s = None
			if style.strip().title() in existing_styles.keys():
				s = existing_styles[style.strip().title()]
			else:
				s = Style.save(style.strip().title())
				existing_styles[s["name"]] = s
			insert_queries.append(ProductStyle.insert_query(product, s, False))
		return existing_styles, insert_queries

	def update_style_line(self, data):
		if "zalora_category_line" not in data.keys():
			return None
		return  data["zalora_category_line"]


	def find_by_sku(self, sku):
		results = self.db.select("products", self.attributes+["description", "current_price_id", "current_discount_id"], [["sku", "=", sku, "String"]])
		if len(results) != 1:
			return None
		return {"id": results[0][0], "category_id": results[0][2], "create_at": results[0][3], "name":results[0][4], "sku":results[0][5], "description":results[0][6], "current_price_id":results[0][7], "current_discount_id":results[0][8]}

	def find_urls_by(self, conditions):
		results = self.db.select("products", ["id", "url", "sku", "description", "current_price_id", "current_discount_id"], conditions)
		output = []
		for r in results:
			output.append({"id": r[0], "url": r[1], "sku": r[2], "description": r[3], "current_price_id": r[4], "current_discount_id": r[5] })
		return output

	def update_description_2(self, id, desc):
		output = []
		for f in desc:
			if f.startswith("-"):
				tmp = [x.strip() for x in f.split("-")]
				output += tmp
			else:
				output.append(f)
		desc = output
		description = "\n".join([x.strip() for x in desc if len(x.strip())>0])
		if len([x.strip() for x in desc if len(x.strip())>0]) ==0:
			description = None
		if description == None:
			self.db.execute("UPDATE PRODUCTS SET description=null where id=\'"+id+"\'")
		else:
			#print "**"
			#print description.replace(u"\u00AE", '&reg;').replace(u"\u00E9", 'e').replace(u"\u2122",'&trad;').replace(u"\ufffd", 'e').replace(u'\u00C3','&').replace(u"\u00E2",'').replace("\'", "''").encode('utf-8')
			self.db.execute("UPDATE PRODUCTS SET description=\'"+description.replace(u"\u00AE", '&reg;').replace(u"\u2122",'&trad;').replace(u"\ufffd", 'e').replace(u"\u00E2",'').replace(u'\u00C3','&').replace(u"\u00E9", 'e').replace("\'", "''").replace('&nbsp;','')+"\' where id=\'"+id+"\'")

	def add_variants(self, variants, prod_id, existing_variants):
		Variant = Variants(self.db)
		product_variants = {}
		if prod_id in existing_variants.keys():
			product_variants = existing_variants[prod_id]
		for var in variants:
			if str(var["variant"]) not in product_variants.keys():
				Variant.save(str(var["variant"]),prod_id, size=var["value"])

	def save_from_json_2(self, data, meta):
		if data["category"] == None or data["sku"]==None or data["name"]==None or data["website_id"]==None:
			return None
		#start = time.time()
		sku =  data["website_id"]+"-"+str(data["sku"])
		gender = None
		if data["gender"] != None:
			if data["gender"].title() not in meta["genders"].keys():
				gender = self.get_or_create_gender_by_name(data["gender"].title())
				data["gender"] = gender
				meta["genders"][gender["name"]] = gender
			else:
				gender = meta["genders"][data["gender"].title()]
		category = None
		if data["category"] != None:
			if data["category"].title() not in meta["categories"].keys():
				category = self.get_or_create_category_by_name(data["category"].title(), gender=gender)
				data["category"] = category
				meta["categories"][category["name"]] = category
			else:
				category = meta["categories"][data["category"].title()]
		brand = None
		if data["brand"] != None:
			if data["brand"] not in meta["brands"].keys():
				brand = self.get_or_create_brand_by_name(data["brand"])
				data["brand"] = brand
				meta["brands"][brand["name"]] = brand
			else:
				brand = meta["brands"][data["brand"]]
		
		description = "\n".join([x.strip() for x in data["features"] if len(x.strip())>0])
		if len([x.strip() for x in data["features"] if len(x.strip())>0]) ==0:
			description = None
		else:
			description = description.encode('utf-8')
		name = data["name"].strip().encode('utf-8')
		color = data["color"]
		if color:
			color = color.title()
		subcategory = None
		if "subcat" in data.keys():
			if data["subcat"] != None:
				if data["subcat"].title() not in meta["categories"].keys():
					subcategory = self.get_or_create_category_by_name(data["subcat"].title(), gender=gender, parent=category)
					meta["categories"][subcategory["name"]] = subcategory
					subcategory = subcategory["id"]
					category = subcategory["category"]
				else:
					subcategory = meta["categories"][data["subcat"].title()]["id"]
					category["id"] = meta["categories"][data["subcat"].title()]["category"]
				
		url = data["url"]
		website = meta["website"]
		style_line = self.update_style_line(data)
		create_at, update_at = self.get_create_date(data)
		product_id = uuid.uuid1().hex
		update_query=[]
		insert_query=[]
		#print "TRANSFORMATION", time.time() - start
		#product = self.find_by_sku(sku)
		if sku in meta["products"].keys():
			product = meta["products"][sku]
			if description!=None:
				if product["description"] == None:
					description = description
				else:
					if len(product["description"])>0 and len(description)>0 and description!=product["description"]:
						description = description
					else:
						description = product["description"]
			else:
				description = product["description"] 
			#self.db.update("products", [["update_at", datetime.datetime.now(), "Date"], ["description", description, "String"], ["color", color, "String"], ["style_line", style_line, "String"]], [["id", "=", product["id"], "String"]])
			update_query = [[[datetime.datetime.now(), "Date"], [description, "String"], [color, "String"], [style_line, "String"], [product["id"], "String"]]]
		else:
			create_at, update_at = self.get_create_date(data)
			product_id = uuid.uuid1().hex
			#self.db.insert("products", self.attributes+self.other_attributes+self.forgotten_attributes+["update_at", "style_line"], [[product_id, "String"], [0, "Int"], [category["id"], "Int"], [create_at, "Date"],[name, "String"],[sku, "String"],[brand["id"], "Int"],[description, "String"], [subcategory, "Int"], [url, "String"], [website["id"], "String"], [gender["id"], "Int"], [color, "String"], [update_at, "Date"], [style_line, "String"]])
			insert_query = [[[product_id, "String"], [0, "Int"], [category["id"], "Int"], [create_at, "Date"],[name, "String"],[sku, "String"],[brand["id"], "Int"],[description, "String"], [subcategory, "Int"], [url, "String"], [website["id"], "String"], [gender["id"], "Int"], [color, "String"], [update_at, "Date"], [style_line, "String"]]]
			product = {"id":product_id, "current_price_id" :None, "current_discount_id":None}
		
		
		start = time.time()
		update_discount_query, insert_prices, update_price_query = self.update_price_2(product, data['price'], data['discount'])
		price_time = time.time()-start
		if price_time > 0.1:
			print "PRICE", price_time
		start = time.time()
		meta["sizes"], update_size_availability, insert_product_sizes, delete_missing_sizes  = self.add_sizes_2(product, data["size"], existing_sizes=meta["sizes"])
		size_time = time.time()-start
		if size_time > 0.1:
			print "SIZE", size_time
		start = time.time()
		insert_images, delete_images = self.add_images_2(product, data["images"])
		image_time = time.time()-start
		if image_time > 0.1:
			print "IMAGE", image_time
		start = time.time()
		meta["styles"], insert_styles, delete_styles, end = self.add_styles_2(product, data, existing_styles=meta["styles"])
		style_time = time.time()-start
		if style_time > 0.1:
			print "STYLE", style_time, data["zalora_subcats"], end

		return product, meta, update_query, insert_query, update_discount_query, insert_prices, update_price_query,  update_size_availability, insert_product_sizes, delete_missing_sizes, insert_images, delete_images, insert_styles, delete_styles


	def save_from_json_3(self, data, meta):
		if data["category"] == None or data["sku"]==None or data["name"]==None or data["website_id"]==None:
			return None
		#start = time.time()
		sku =  data["website_id"]+"-"+str(data["sku"])
		gender = None
		if data["gender"] != None:
			if data["gender"].title() not in meta["genders"].keys():
				gender = self.get_or_create_gender_by_name(data["gender"].title())
				data["gender"] = gender
				meta["genders"][gender["name"]] = gender
			else:
				gender = meta["genders"][data["gender"].title()]
		category = None
		if data["category"] != None:
			if data["category"].title() not in meta["categories"].keys():
				category = self.get_or_create_category_by_name(data["category"].title(), gender=gender)
				data["category"] = category
				meta["categories"][category["name"]] = category
			else:
				category = meta["categories"][data["category"].title()]
		brand = None
		if data["brand"] != None:
			if data["brand"] not in meta["brands"].keys():
				brand = self.get_or_create_brand_by_name(data["brand"])
				data["brand"] = brand
				meta["brands"][brand["name"]] = brand
			else:
				brand = meta["brands"][data["brand"]]

		need_additional_data = False
		if data["website_id"] == "zalora" or data["website_id"] == "asos":
			need_additional_data = True
		
		description = "\n".join([x.strip() for x in data["features"] if len(x.strip())>0])
		if len([x.strip() for x in data["features"] if len(x.strip())>0]) ==0:
			description = None
		else:
			description = description.encode('utf-8')
		name = data["name"].strip().encode('utf-8')
		color = data["color"]
		if color:
			color = color.title()
		subcategory = None
		if "subcat" in data.keys():
			if data["subcat"] != None:
				if data["subcat"].title() not in meta["categories"].keys():
					subcategory = self.get_or_create_category_by_name(data["subcat"].title(), gender=gender, parent=category)
					meta["categories"][subcategory["name"]] = subcategory
					subcategory = subcategory["id"]
				else:
					subcategory = meta["categories"][data["subcat"].title()]["id"]
				
		url = data["url"]
		website = meta["website"]
		style_line = self.update_style_line(data)
		create_at, update_at = self.get_create_date(data)
		product_id = uuid.uuid1().hex
		update_query=[]
		insert_query=[]
		#print "TRANSFORMATION", time.time() - start
		#product = self.find_by_sku(sku)
		if sku in meta["products"].keys():
			product = meta["products"][sku]
			if description!=None:
				if product["description"] == None:
					description = description
				else:
					if len(product["description"])>0 and len(description)>0 and description!=product["description"]:
						description = description
					else:
						description = product["description"]
			else:
				if "description" in product.keys():
					description = product["description"] 
				else:
					description = None
			#self.db.update("products", [["update_at", datetime.datetime.now(), "Date"], ["description", description, "String"], ["color", color, "String"], ["style_line", style_line, "String"]], [["id", "=", product["id"], "String"]])
			update_query = [[[datetime.datetime.now(), "Date"], [description, "String"], [color, "String"], [style_line, "String"], [product["id"], "String"]]]
		else:
			create_at, update_at = self.get_create_date(data)
			product_id = uuid.uuid1().hex
			#self.db.insert("products", self.attributes+self.other_attributes+self.forgotten_attributes+["update_at", "style_line"], [[product_id, "String"], [0, "Int"], [category["id"], "Int"], [create_at, "Date"],[name, "String"],[sku, "String"],[brand["id"], "Int"],[description, "String"], [subcategory, "Int"], [url, "String"], [website["id"], "String"], [gender["id"], "Int"], [color, "String"], [update_at, "Date"], [style_line, "String"]])
			need_process = True
			insert_query = [[[product_id, "String"], [0, "Int"], [category["id"], "Int"], [create_at, "Date"],[name, "String"],[sku, "String"],[brand["id"], "Int"],[description, "String"], [subcategory, "Int"], [url, "String"], [website["id"], "String"], [gender["id"], "Int"], [color, "String"], [update_at, "Date"], [style_line, "String"], [need_additional_data, "Boolean"], [need_process, "Boolean"]]]
			product = {"id":product_id, "current_price_id" :None, "current_discount_id":None}
		
		
		start = time.time()
		update_discount_query, insert_prices, update_price_query = self.update_price_2(product, data['price'], data['discount'])
		price_time = time.time()-start
		if price_time > 0.1:
			print "PRICE", price_time
		start = time.time()
		variants = {}
		if product["id"] in meta["variants"].keys():
			variants = meta["variants"][product["id"]]
		meta["sizes"], insert_product_sizes, need_find_variant = self.add_sizes_3(product, data["size"], existing_sizes=meta["sizes"], existing_variants=variants)
		size_time = time.time()-start
		if size_time > 0.1:
			print "SIZE", size_time
		start = time.time()
		insert_images = self.add_images_3(product, data["images"])
		image_time = time.time()-start
		if image_time > 0.1:
			print "IMAGE", image_time
		start = time.time()
		meta["styles"], insert_styles = self.add_styles_3(product, data, existing_styles=meta["styles"])
		style_time = time.time()-start
		if style_time > 0.1:
			print "STYLE", style_time

		return product, meta, update_query, insert_query, update_discount_query, insert_prices, update_price_query, insert_product_sizes, insert_images, insert_styles

	def update_price_2(self, product, price, discount):
		current_price, current_discount = None, None
		if "current_price_id" in product.keys() and product["current_price_id"]!=None:
			current_price = self.get_price_by_id(product["current_price_id"])
		if "current_discount_id" in product.keys() and product["current_discount_id"]!=None:
			current_discount = self.get_price_by_id(product["current_discount_id"])

		insert_prices = []
		update_price_query=[]
		update_discount_query=[]
		end_promotion = False
		if current_discount != None and (len(discount)==0 or discount==None):
			end_promotion = True

		if len(discount)==0 or discount==None:
			#self.db.update("products", [["current_discount_id", None, "String"]], [["id", '=', product["id"], "String"]])
			update_discount_query = [[[None, "String"],[product["id"], "String"]]]

		if len(price)>0:
			if end_promotion == True or current_price == None:
				price = self.add_price_2(product, price[0])
				insert_prices.append(price)
			if end_promotion == False and current_price != None:
				if isinstance(price[0]["price"], basestring):
					if "," in price[0]["price"] and "." in price[0]["price"]:
						price[0]["price"] = price[0]["price"].replace(",","")
				if current_price["value"] == float(price[0]["price"]) and current_price["currency"] == price[0]["currency"]:
					price = [[current_price["id"]]]
				else:
					price = self.add_price_2(product, price[0])
					insert_prices.append(price)
			if price:
				#self.db.update("products", [["current_price_id", price["id"], "String"]], [["id", '=', product["id"], "String"]])
				update_price_query = [[[price[0][0], "String"], [product["id"], "String"]]]

		if len(discount)>0:
			if current_discount != None:
				if isinstance(discount[0]["price"], basestring):
					if "," in discount[0]["price"] and "." in discount[0]["price"]:
						discount[0]["price"] = discount[0]["price"].replace(",","")
				if current_discount["value"] == float(discount[0]["price"]) and current_discount["currency"] == discount[0]["currency"]:
					discount =   [[current_discount["id"]]] 
				else:
					discount = self.add_price_2(product, discount[0], is_discount=True)
					insert_prices.append(discount)
			else:
				discount = self.add_price_2(product, discount[0], is_discount=True)
				insert_prices.append(discount)
			if discount:
				#self.db.update("products", [["current_discount_id", discount["id"], "String"]], [["id", '=', product["id"], "String"]])
				update_discount_query = [[[discount[0][0], "String"],[product["id"], "String"]]]
		#self.db.commit()
		return update_discount_query, insert_prices, update_price_query

	def save_all(self, update_queries, insert_queries, update_discount_queries,insert_prices_queries,update_price_queries,update_size_availability_queries,insert_product_sizes_queries,delete_missing_sizes_queries,insert_images_queries,delete_images_queries,insert_styles_queries,delete_styles_queries):
		print "INSERTING PRODUCTS", len(update_queries)+len(insert_queries)
		self.db.execute_many_updates("products", ["update_at", "description", "color", "style_line"], [["id", "="]], update_queries)
		self.db.execute_many_inserts("products", self.attributes+self.other_attributes+self.forgotten_attributes+["update_at", "style_line"]+["need_additional_data", "need_process"], insert_queries)
		product_ids = [ x[-1][0] for x in update_queries] + [ x[0][0] for x in insert_queries]
		product_ids = []
		
		print "INSERTING PRICES", len(insert_prices_queries)+len(update_discount_queries)+len(update_price_queries)
		Price = Prices(self.db)
		Price.insert_many(insert_prices_queries)
		self.db.execute_many_updates("products", ["current_discount_id"], [["id", "="]], update_discount_queries)
		self.db.execute_many_updates("products", ["current_price_id"], [["id", "="]], update_price_queries)

		print "INSERTING SIZES", len(update_size_availability_queries)+len(insert_product_sizes_queries)+len(delete_missing_sizes_queries)
		ProductSize = ProductSizes(self.db)
		ProductSize.update_many_availability(update_size_availability_queries)
		ProductSize.insert_many(insert_product_sizes_queries)
		ProductSize.delete_many(delete_missing_sizes_queries)

		print "INSERTING IMAGES", len(insert_images_queries)+len(delete_images_queries)
		Image = Images(self.db)
		Image.insert_many(insert_images_queries)
		Image.delete_many(delete_images_queries)

		print "INSERTING STYLES", len(insert_styles_queries)+len(delete_styles_queries)
		#print insert_styles_queries
		ProductStyle = ProductStyles(self.db)
		ProductStyle.insert_many(insert_styles_queries)
		ProductStyle.delete_many(delete_styles_queries)

		return product_ids

	def save_all_3(self, update_queries, insert_queries, update_discount_queries,insert_prices_queries,update_price_queries,insert_product_sizes_queries,insert_images_queries,insert_styles_queries):
		print "INSERTING PRODUCTS", len(update_queries)+len(insert_queries)
		self.db.execute_many_updates("products", ["update_at", "description", "color", "style_line"], [["id", "="]], update_queries)
		self.db.execute_many_inserts("products", self.attributes+self.other_attributes+self.forgotten_attributes+["update_at", "style_line"]+["need_additional_data", "need_process"], insert_queries)
		product_ids = [ x[-1][0] for x in update_queries] + [ x[0][0] for x in insert_queries]
		product_skus = { x[5][0] : { "id": x[0][0] } for x in insert_queries }
		
		print "INSERTING PRICES", len(insert_prices_queries)+len(update_discount_queries)+len(update_price_queries)
		Price = Prices(self.db)
		Price.insert_many(insert_prices_queries)
		self.db.execute_many_updates("products", ["current_discount_id"], [["id", "="]], update_discount_queries)
		self.db.execute_many_updates("products", ["current_price_id"], [["id", "="]], update_price_queries)

		print "INSERTING SIZES", len(insert_product_sizes_queries)
		ProductSize = ProductSizes(self.db)
		ProductSize.insert_many(insert_product_sizes_queries)

		print "INSERTING IMAGES", len(insert_images_queries)
		Image = Images(self.db)
		Image.insert_many(insert_images_queries)

		print "INSERTING STYLES", len(insert_styles_queries)
		#print insert_styles_queries
		ProductStyle = ProductStyles(self.db)
		ProductStyle.insert_many(insert_styles_queries)

		return product_ids, product_skus

	def delete_all(self, product_ids, website):
		print "DELETING", len(product_ids)
		if len(product_ids) == 0:
			return
		self.db.execute("delete from images where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
		self.db.execute("delete from product_sizes where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
		self.db.execute("delete from product_styles where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
		self.db.execute("update products set current_price_id = null, current_discount_id=null where id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
		self.db.execute("delete from prices where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
		self.db.execute("delete from products where id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")

	def prepare_for_new_data(self, product_ids):
		print "PREPARING DATA", len(product_ids)
		if len(product_ids)>0:
			self.db.execute("delete from product_sizes where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
			self.db.execute("delete from product_styles where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")
			self.db.execute("delete from images where product_id in ("+",".join(["\'"+str(x)+"\'" for x in product_ids])+")")


# db = db()
# Product = Products(db)

# item = {
#     "category": "Dresses",
#     "sku": "83813",
#     "name": "Sleeveless Fluted Hem Dress (Sand)",
#     "color": "Sand",
#     "gender": "women",
#     "brand": "Dressabelle",
#     "website_id": "dressabelle",
#     "is_new": False,
#     "last_update": "18-05-02 22:55",
#     "discount": [],
#     "features": [
#       "Polyester",
#       "Zip back",
#       "Unlined, non sheer",
#       "Non stretchable"
#     ],
#     "url": "https://www.dressabelle.com.sg/dsb/shop-all/dresses/minikneelengthdresses/sleeveless-fluted-hem-dress-sand-detail.html",
#     "images": [
#       "https://static.dressabelle.com.sg/images/stories/virtuemart/product/resized/dsb838180319059_400x800.jpg",
#       "https://static.dressabelle.com.sg/images/stories/virtuemart/product/resized/dsb838180319058_400x800.jpg",
#       "https://static.dressabelle.com.sg/images/stories/virtuemart/product/resized/dsb838180319062_400x800.jpg",
#       "https://static.dressabelle.com.sg/images/stories/virtuemart/product/resized/dsb838180319060_400x800.jpg",
#       "https://static.dressabelle.com.sg/images/stories/virtuemart/product/resized/dsb838180319063_400x800.jpg"
#     ],
#     "main_picture": "https://static.dressabelle.com.sg/images/stories/virtuemart/product/resized/dsb838180319059_400x800.jpg",
#     "price": [
#       {
#         "currency": "SG$",
#         "price": "44.90",
#         "start_date": "18-05-02 00:00"
#       }
#     ],
#     "size": [
#       {
#         "available": True,
#         "value": "S"
#       },
#       {
#         "available": True,
#         "value": "M"
#       },
#       {
#         "available": True,
#         "value": "L"
#       }
#     ]
#   }


# Product.save_from_json(item)