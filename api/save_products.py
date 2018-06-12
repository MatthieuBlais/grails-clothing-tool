from domain.Products import Products
from domain.DatabaseConnector import DatabaseConnector as dtb
import json
import sys
import logging
from os import listdir
from os.path import isfile, join
import datetime 


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/ec2-user/crawlers/api/logs/save_products.log',
                    filemode='a+')


def list_files(folder_path):
	return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

def load_data(path):
	return json.load(open(path))

def save_products(products):
	db = dtb()
	Product = Products(db)
	saved_items = {}
	error_items = []
	count = 0
	total = 0
	for product in products:
		try:
			item = Product.save_from_json(product)
			if item["category"]["name"]+"_"+str(item["category"]["gender"]) not in saved_items.keys():
				saved_items[item["category"]["name"]+"_"+str(item["category"]["gender"])] = 0
			saved_items[item["category"]["name"]+"_"+str(item["category"]["gender"])] +=1
			count+=1
		except:
			raise
			error_items.append(product)
			logging.error('SAVING PRODUCT: '+str(json.dumps(product)))
		total+=1
		print count, len(products)
		if total % 50 == 0:
			logging.info('SAVING PRODUCTS: '+str(total)+"/"+str(len(products)))

	return { "success": saved_items, "error": error_items, "error_total": len(error_items), "success_total":count}

def save_report(report, f):
	f = f.split("/")[-1]
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	with open("/home/ec2-user/crawlers/api/logs/"+date+f, "w+") as logfile:
		json.dump(report, logfile)

if __name__ == "__main__":
	logging.info('STARTING: listing files in '+sys.argv[1])
	files = list_files(sys.argv[1])
	logging.info('LISTING FILES: '+str(len(files)))

	for f in files:
		logging.info('READING FILE: '+f)
		products = load_data(f)
		logging.info('SAVING PRODUCTS: '+str(len(products))+" products")
		report = save_products(products)
		logging.info('SAVING PRODUCTS DONE: '+str(json.dumps(report)))
		save_report(report, f)


