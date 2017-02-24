import pymongo
import time


###########
	# DB
###########
def generate_client(client):
	database_name = ''
	if 'database' in client:
		database_name = client['database']

	print(client)
	if 'host' in client:
		host = client['host']
	if 'port' in client:
		port = client['port']

	if 'user' in client:
		user = client['user']
		if 'pwd' in client:
			pwd = client['pwd']
		else:
			return pymongo.MongoClient("mongodb://"+user+"@"+host+":"+str(port)+"/"+database_name)
	else:
		return pymongo.MongoClient("mongodb://"+host+":"+str(port)+"/"+database_name)

	return pymongo.MongoClient("mongodb://"+user+":"+pwd+"@"+host+":"+str(port)+"/"+database_name)


def get_distinct_place_ids(client_info):
	client = generate_client(client_info)

	database = client[client_info['database']]
	collection = database[client_info['collection']]

	return collection.distinct('place_id')


###########
	# Cursor
###########
def GetNext(cursor):
	return next(cursor,None)