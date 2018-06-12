from domain.Products import Products
from domain.Websites import Websites
from domain.DatabaseConnector import DatabaseConnector as dtb
import json
import sys
import logging
from os import listdir
from os.path import isfile, join
import datetime 

current_path="./"
#destination_path='/home/ec2-user/crawlers/'+sys.argv[1]+"/"+sys.argv[1]+"/input/"
#destination_path='../../crawlers/'+sys.argv[1]+"/"+sys.argv[1]+"/input/"
destination_path="./"

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s',
#                     filename='/home/ec2-user/crawlers/api/logs/load_sku.log',
#                     filemode='a+')

zalora_conditions = [["description", "is", "null", "Int"]]
asos_conditions = []

def find_website(name):
	db = dtb()
	Website = Websites(db)
	return Website.find_by_name(name)

def find_products(website):
	db = dtb()
	Product = Products(db)
	conditions = [["website_id", "=", website["id"], "String"]]
	if website["name"] == "zalora":
		conditions += zalora_conditions
	return Product.find_urls_by(conditions)

def split_products(products):
	if len(products)<10000:
		return [products]
	output = []
	total_files = (len(products) - (len(products)%10000)) / 10000
	modulo = len(products)%10000
	for i in range(total_files):
		output.append(products[(i*10000):((i+1)*10000)])
	if modulo != 0:
		output.append(products[(total_files*10000):])
	return output

def save_products(products):
	for i in range(len(products)):
		with open(destination_path+str(i)+".json", "w+") as prodFile:
			json.dump(products[i], prodFile)
	
if __name__ == "__main__":
	logging.info('STARTING: Getting website '+sys.argv[2])
	website = find_website(sys.argv[2])
	logging.info('FINDING PRODUCTS')
	products = find_products(website)
	products = split_products(products)
	save_products(products)