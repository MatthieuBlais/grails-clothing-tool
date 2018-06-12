import psycopg2
import json
from os import listdir
from os.path import isfile, join
import datetime

def list_files(folder_path):
	return [join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path, f))]

def load_data(path):
	return json.load(open(path))

def extract_url(query):
	query = query.split("VALUES (")[1]
	query = query.split(",")[2]
	return query.strip().replace("'", "")

def is_main(query):
	query = query.split("VALUES (")[1]
	query = query.split(",")[12]
	return query.strip() == "true"

def confidence(query):
	query = query.split("VALUES (")[1]
	query = query.split(",")[11]
	return float(query)

def replace_id(query, next_id):
	splitted = query.split("VALUES (")
	comma_splitted = splitted[1].split(",")
	comma_splitted = comma_splitted[1:]
	return splitted[0]+"VALUES ("+str(next_id)+","+",".join(comma_splitted)

def stringToBoolean(s):
	if s.lower() == "true":
		return True
	return False

def as_tuples(queries):
	tuples = []
	for query in queries:
		query = query.split("VALUES (")
		query = query[1].split(")")
		data = query[0].split(",")
		data = [x.strip() for x in data]
		tpl = (int(data[0]), int(data[1]), data[2].replace("\'",""), data[3].replace("\'",""), data[4].replace("\'",""), data[5].replace("\'",""), float(data[6]), float(data[7]), float(data[8]), float(data[9]), data[10].replace("\'",""), float(data[11]), stringToBoolean(data[12].strip()), int(data[13]), int(data[14]), stringToBoolean(data[15].strip()), None, datetime.datetime.strptime(data[17].replace("\'","").strip(), '%Y-%m-%d %H:%M:%S.%f'))
		tuples.append(tpl)
	return tuples

def execute_queries(queries, db):
	# for i in range(0,len(queries)):
	# 	db.insert(queries[i])
	# 	print i, len(queries)
	query = "INSERT INTO object_detections (id, version, url, local_path, no_background_path, cropped_name, x_min, x_max, y_min, y_max, label, condidence, was_expected, height, width, is_validated, is_wrong, detection_date) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	db.insertmany(query, queries)

def next_id(db):
	return db.select_next_id("object_detections")

class DatabaseConnector(object):
	"""docstring for DatabaseConnector"""
	def __init__(self, connection_string="host='matthieu.c9ugkbttzgdh.ap-southeast-1.rds.amazonaws.com' dbname='meow' user='crawler' password='M4ch4tt3!'"):
		super(DatabaseConnector, self).__init__()
		#connection_string="host='localhost' dbname='meow' user='dashboard' password='3006Jollibee'"
		self.conn_string = connection_string
		self.con = psycopg2.connect(self.conn_string)
		self.cur = self.con.cursor()
	

	def execute(self, query):
		self.cur.execute(query)
		result = self.cur.fetchall()
		return result

	def insertmany(self, query, data):
		self.cur.executemany(query, data)

	def insert(self, query):
		self.cur.execute(query)

	def select_next_id(self, table):
		query="SELECT MAX(id) FROM "+table 
		self.cur.execute(query)
		results = self.cur.fetchone()
		if results[0] == None:
			return 1
		else:
			return results[0]+1

	def commit(self):
		self.con.commit()


files = list_files("../../../tmp/queries")

last_files = [x for x in files if x.startswith("../../../tmp/queries/queries_"+str(len(files)-1))]
last_files = sorted(last_files)
last_files = last_files[-1]

db = DatabaseConnector()

next_id = next_id(db)


to_append = None
for i in range(0, len(files)):
	## LOAD DATA
	print "LOADING DATA"
	if i < (len(files)-2):
		current_data = load_data("../../../tmp/queries/queries_"+str((i+1)*1000)+".json")
		next_data = load_data("../../../tmp/queries/queries_"+str((i+2)*1000)+".json")
	else:
		current_data = load_data(last_files)
		next_data = []

	## ONLY KEEP ONE MAIN AND ONE OTHER 
	print "FILTERING"
	dico_queries = {}
	if to_append != None:
		dico_queries[to_append["key"]] = to_append["data"]
	for j in range(0, len(current_data)):
		url = extract_url(current_data[j])
		if url not in dico_queries.keys():
			dico_queries[url] = {}
		if is_main(current_data[j]):
			dico_queries[url]["main"] = current_data[j]
		else:
			if "confidence" in dico_queries[url].keys():
				if dico_queries[url]["confidence"] < confidence(current_data[j]):
					dico_queries[url]["confidence"] = confidence(current_data[j])
					dico_queries[url]["other"] = current_data[j]
			else:
				dico_queries[url]["confidence"] = confidence(current_data[j])
				dico_queries[url]["other"] = current_data[j]

		if j == len(current_data) -1:
			if len([x for x in next_data if url in x])>0:
				to_append = {"data": dico_queries[url], "key": url}
				dico_queries.pop(url, None)

	## FORMAT FROM DICO TO ARRAY
	print "FORMAT DATA"
	queries = []
	for k in dico_queries.keys():
		if "main" in dico_queries[k].keys():
			queries.append(replace_id(dico_queries[k]["main"],next_id))
			next_id+=1
		if "other" in dico_queries[k].keys():
			queries.append(replace_id(dico_queries[k]["other"],next_id))
			next_id+=1
	queries = as_tuples(queries)
	print "INSERTING DATA"
	execute_queries(queries, db)

	print "FILE", i, len(files)


db.commit()





