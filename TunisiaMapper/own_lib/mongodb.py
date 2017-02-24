import pymongo
import time
	
client = None

database = None
database_name = 'LikwidBotDB'

host = 'localhost'
port = 27017

user = 'likwidbot'
pwd = 'iamthebot'


def end_iter(loops):
	print("ending loop number: "+str(loops[-1:]))
	loops.append(len(loops))
	return loops

def generate_client(client):
	database_name = ''
	if 'database' in client:
		database_name = client['database']

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


def save_to_database(client,database,collection,document):
	client = generate_client(client)

	database = client[database]
	collection = database[collection]
	collection.insert(document)

	return collection.find_one(document)

def update_place(client,database,collection,document):
	client = generate_client(client)

	database = client[database]
	collection = database[collection]

	requests = [pymongo.ReplaceOne({'place_id': document['place_id']}, upsert=False)]
	collection.bulk_write(requests)
	


def get_place(client,database,collection,place_id):

	client = generate_client(client)

	collection = client[database][collection]
	rslt = collection.find_one({'place_id':place_id})
	
	return rslt


def store_place(country,state,place,keyword,client):
	try:
		to_save = {}
		to_save['country'] = country
		to_save['state'] = state
		to_save.update(place)
		to_save['tags'] = [keyword]

		database = client['database']
		collection = client['collection']

		rslt = get_place(client,client['database'],collection,place['place_id'])
		print("result of query: "+str(rslt))

		if rslt is None:
			r = save_to_database(client,database,collection,to_save)
		else:
			if 'tags' in rslt['tags']:
			    for tag in rslt['tags']:
			        to_save['tags'].append(tag)
			r = update_place(client,database,collection,to_save)
	except Exception as exc:
		raise(exc)


	return r['_id']
