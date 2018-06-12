from domain.Products import Products
from domain.Variants import Variants
from domain.DatabaseConnector import DatabaseConnector as dtb
import json
import sys
import logging
from os import listdir
from os.path import isfile, join
import datetime 

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s',
#                     filename='/home/ec2-user/crawlers/api/logs/save_products.log',
#                     filemode='a+')

def list_files(folder_path):
	return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

def load_data(path):
	return json.load(open(path))

def load_variants(db):
	Variant = Variants(db)
	variants = Variant.find_all()
	return variants

if __name__ == "__main__":
	logging.info('STARTING: listing files in '+sys.argv[1])
	files = list_files(sys.argv[1])
	logging.info('LISTING FILES: '+str(len(files)))
	files = [files[-1]]
	db = dtb()
	Product = Products(db)
	variants = load_variants(db)
	for f in files:
		logging.info('READING FILE: '+str(f))
		print 'READING FILE: '+str(f)
		products = load_data(f)
		counter = 0
		for prod in products:
			description = []
			if "description" in prod.keys():
				description = prod["description"]
			else:
				description = prod["features"]
			Product.update_description_2(prod["id"], description)
			# if "images" in prod.keys():
			# 	Product.add_images({"id":prod["id"]}, prod["images"])
			if "size" in prod.keys():
				# Product.add_sizes({"id":prod["id"]}, prod["size"])
				Product.add_variants(prod["size"], prod["id"], variants)
			counter+=1
			print counter, len(products)
		db.commit()
		


