import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import sys
from datetime import datetime, timedelta

class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)

websites = json.loads(sys.argv[1])
websites = websites["websites"]

today = datetime.today()


data = [] 

dynamodb = boto3.resource("dynamodb", region_name='ap-southeast-1')
table = dynamodb.Table('meow_crawlers')

for website in websites:
	last_update = None
	for i in range(0,4):
		date = today - timedelta(days=(3-i))
		date = date.strftime('%Y-%m-%d')

		try:
			response = table.get_item(
				Key={
				'website_id': website,
				'date': date
				}
			)
		except ClientError as e:
			print(e.response['Error']['Message'])
		else:
			if 'Item' in response.keys():
				item = response['Item']
				last_update = item
	if last_update != None:
		data.append(last_update)
	else:
		data.append({ "website_id": website, "start": "ERROR", "stop": "ERROR", "skus":0, "total":0, "details":{}})


print json.dumps(data,cls=DecimalEncoder)