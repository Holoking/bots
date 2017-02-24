import pymongo
import time

###########
	# Cursor
###########
def getNext(cursor):
	nxt = next(cursor,None)
	print('next target: '+str(nxt))
	return nxt 



###########
	# Database
###########
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


def storeAnalysis(redacted,target,action,document,client_infos):
	print()
	print()
	print(target)
	if not redacted:
		client = generate_client(client_infos)
		database = client[client_infos['database']]
		collection = database[client_infos['collection']]

		to_save = {}
		to_save['analysis_type'] = action['command']

		parameters = {}
		parameters.update(action['parameters'])
		parameters.pop('fb_access_token',None)
		parameters.pop('fb_token_version',None)
		parameters.pop('headers',None)
		parameters.pop('base_url',None)

		to_save['parameters'] = {}
		to_save['parameters'].update(parameters)
		to_save['results'] = document
		to_save['time'] = time.time()

		to_save['target_id'] = target['_id']

		collection.insert(to_save)


def get_targets(client_infos):
	client = generate_client(client_infos)
	database = client[client_infos['database']]
	collection = database[client_infos['collection']]
	return collection.find()


def saveReport(target,report,client_infos):
	client = generate_client(client_infos)
	database = client[client_infos['database']]
	collection = database[client_infos['collection']]

	if report['conclusion'] != 'go':
		to_save = {}
		# Clean data before storag
		to_save.update(report)
		to_save.update({'target_id':target['_id']})

		collection.insert(to_save)




