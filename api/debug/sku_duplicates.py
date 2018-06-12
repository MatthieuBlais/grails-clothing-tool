import json 


data = json.load(open('../data/data2.json'))



brands = []
skus = []
urls = {}
same = 0
for d in data:
	if d["brand"] not in brands:
		brands.append(d["brand"])
	if d["sku"] not in skus:
		skus.append(d["sku"])
		urls[d["sku"]] = d["url"]
	else:
		#print d["url"], urls[d["sku"]]
		if urls[d["sku"]] != d["url"]:
			print urls[d["sku"]], d["url"]
		else:
			same += 1


print len(skus)
print same

print len(brands)