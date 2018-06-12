from domain.Products import Products
from domain.DatabaseConnector import DatabaseConnector as dtb
import json
import sys
import logging
from os import listdir
from os.path import isfile, join
import datetime 
from domain.Categories import Categories
from domain.Brands import Brands
from domain.Websites import Websites
from domain.Sizes import Sizes 
from domain.Genders import Genders
from domain.Styles import Styles
from domain.Variants import Variants
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s',
#                     filename='/home/ec2-user/crawlers/api/logs/save_products.log',
#                     filemode='a+')


def list_files(folder_path):
	return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

def load_data(path):
	return json.load(open(path))

def find_website(name):
	db = dtb()
	Website = Websites(db)
	website = Website.find_by_name(name.strip())
	if not website:
		website = Website.save(name.strip())
		db.commit()
	if not website:
		return None
	return website

def load_existing_products(db, website):
	if website == None:
		return {}
	Product = Products(db)
	conditions = [["website_id", "=", website["id"], "String"]]
	products= Product.find_urls_by(conditions)
	return { x["sku"] : x for x in products }

def load_metadata(website):
	db = dtb()
	Gender = Genders(db)
	genders = Gender.find_all()
	Category = Categories(db)
	categories = Category.find_all()
	Brand = Brands(db)
	brands = Brand.find_all()
	website = website
	products = load_existing_products(db, website)
	Size = Sizes(db)
	sizes = Size.find_all()
	Style = Styles(db)
	styles = Style.find_all()
	Variant = Variants(db)
	variants = Variant.find_all()
	return { "genders": genders, "categories": categories, "brands": brands, "website":website, "products":products, "sizes": sizes, "styles":styles, "variants":variants}


def insert_all(db, update_queries, insert_queries, update_discount_queries,insert_prices_queries,update_price_queries,update_size_availability_queries,insert_product_sizes_queries,delete_missing_sizes_queries,insert_images_queries,delete_images_queries,insert_styles_queries,delete_styles_queries):
	db.executemany()


def clean_data(db, products, website, existing_products):
	skus = list(set([data["website_id"]+"-"+str(data["sku"]) for data in products]))
	product_ids = [existing_products[x]["id"] for x in existing_products.keys() if x in skus]
	Product = Products(db)
	Product.prepare_for_new_data(product_ids)




def save_products(products, meta, product_ids=[]):
	db = dtb()
	Product = Products(db)
	saved_items = {}
	error_items = []
	count = 0
	total = 0
	update_queries = []
	insert_queries = []
	update_discount_queries = []
	insert_prices_queries = []
	update_price_queries= []
	insert_product_sizes_queries= []
	insert_images_queries= []
	insert_styles_queries= []
	clean_data(db, products, meta["website"], meta["products"])
	for product in products:
		try:
			item, meta, update_query, insert_query, update_discount_query, insert_prices, update_price_query,  insert_product_sizes, insert_images, insert_styles = Product.save_from_json_3(product, meta)
			update_queries += update_query
			insert_queries += insert_query
			update_discount_queries += update_discount_query
			insert_prices_queries += insert_prices
			update_price_queries += update_price_query
			insert_product_sizes_queries += insert_product_sizes
			insert_images_queries += insert_images
			insert_styles_queries += insert_styles
			#print insert_images
			count+=1
		except:
			raise
			error_items.append(product)
			logging.error('SAVING PRODUCT: '+str(json.dumps(product)))
		total+=1
		print count, len(products)
		if total % 50 == 0:
			logging.info('SAVING PRODUCTS: '+str(total)+"/"+str(len(products)))

	pids, pskus = Product.save_all_3(update_queries, insert_queries, update_discount_queries,insert_prices_queries,update_price_queries,insert_product_sizes_queries,insert_images_queries,insert_styles_queries)
	product_ids += pids
	for k in pskus.keys():
		if k not in meta["products"].keys():
			meta["products"][k] = pskus[k]
	db.commit()

	return { "success": saved_items, "error": error_items, "error_total": len(error_items), "success_total":count}, product_ids, meta

def extract_existing_ids(products, existing_products):
	return [ products[x]["id"] for x in products.keys() if products[x]["id"] not in existing_products] + existing_products

def delete_products(product_ids, website):
	db = dtb()
	Product = Products(db)
	Product.delete_all(product_ids, website)
	db.commit()


# def save_report(report, f):
# 	f = f.split("/")[-1]
# 	date = datetime.datetime.now().strftime("%Y-%m-%d")
# 	with open("/home/ec2-user/crawlers/api/logs/"+date+f, "w+") as logfile:
# 		json.dump(report, logfile)

if __name__ == "__main__":
	logging.info('STARTING: listing files in '+sys.argv[1])
	files = list_files(sys.argv[1])
	logging.info('LISTING FILES: '+str(len(files)))
	website = find_website(sys.argv[2])
	
	counter = 1
	product_ids = []
	existing_products = []
	print "LOADING METADATA"
	meta = load_metadata(website)
	print "EXTRACT EXISTING IDS"
	existing_products = extract_existing_ids(meta["products"], existing_products)
	for f in files:
		#if counter>12:
		logging.info('READING FILE: '+f)
		print "READING FILE"
		products = load_data(f)
		logging.info('SAVING PRODUCTS: '+str(len(products))+" products")
		report, product_ids, meta = save_products(products, meta, product_ids)
		logging.info('SAVING PRODUCTS DONE: '+str(json.dumps(report)))
		counter+=1
		print counter, len(files)
		#save_report(report, f)
	if website != None and len(existing_products)>0:
		if float(len(product_ids))/float(len(existing_products))>0.6:
			to_delete = [x for x in existing_products if x not in product_ids]
			delete_products(to_delete, website)


