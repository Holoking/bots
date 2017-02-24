import pymongo
import time
import random
import string
import sha

client = None

database = None
database_name = 'LikwidBotDB'

host = 'localhost'
port = 27017

user = 'likwidbot'
pwd = 'iamthebot'

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

	collection.update({'_id':document['_id']}, {"$set": document}, upsert=False)
	


def get_place(client,database,collection,place_id):

	client = generate_client(client)

	collection = client[database][collection]
	rslt = collection.find_one({'place_id':place_id})
	
	return rslt


def generate_identifier(place_id):
	tohash = str(place_id)
	length = random.randint(5,10)
	i = 0

	while i < length:
		tohash += random.choice(string.letters)
		i+=1

	return sha.new(tohash).hexdigest()


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
		if rslt is None:
			likid = generate_identifier(place['place_id'])
			while get_place_by_likw_id(client,client['database'],collection,likid):
				likid = generate_identifier(place['place_id'])

			to_save['likwid_id'] = likid
			save_to_database(client,database,collection,to_save)

		elif 'tags' in rslt:
			update = False
			for tag in rslt['tags']:
				if not tag in to_save['tags']:
					to_save['tags'].append(tag)
					update = True
			to_save['likwid_id'] =  rslt['likwid_id']
			to_save['_id'] = rslt['_id']
			if update:
				r = update_place(client,database,collection,to_save)
		else:
			raise Exception('Unexpected document format.')
	except Exception as exc:
		raise(exc)
