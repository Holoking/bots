import pymongo
import time
	
client = None

database = None
database_name = 'LikwidBotDB'

host = 'localhost'
port = 27017

user = 'likwidbot'
pwd = 'iamthebot'


###########
	# Cursor
###########
def GetNext(cursor):
	return next(cursor,None)




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


def save_to_database(client,database,collection,document):
	client = generate_client(client)
	database = client[database]
	collection = database[collection]
	collection.insert(document)

	return collection.find_one(document)

def update_in_database(client,database,collection,document):
	client = generate_client(client)
	database = client[database]
	collection = database[collection]
	collection.save(document)

	return collection.find_one(document)

def get_place_by_instagram_id(client,database,place_id):
	client = generate_client(client)

	collection = client[database]['places']
	rslt = collection.find_one({'instagram_id':place_id})
	
	return rslt



def get_place_to_analyse_by_instagram(client,database):
	client = generate_client(client)
	collection_instagram= client[database]['instagram']
	collection_places = client[database]['places']
	distinct_instagram_places=collection_instagram.distinct('place_id')

	rslt = collection_places.find({"_id": {'$nin':distinct_instagram_places} })
	print(rslt)
	return rslt

def get_place_to_analyse_by_twitter(client,database):
	client = generate_client(client)
	collection_twitter= client[database]['twitter']
	collection_places = client[database]['places']
	distinct_twitter_places=collection_twitter.distinct('place_id')

	rslt = collection_places.find({"_id": {'$nin':distinct_twitter_places} })
	
	return rslt
def get_place_to_analyse_by_fb_ads(client,database):
	client = generate_client(client)
	collection_fb= client[database]['facebook_ads']
	collection_instagram = client[database]['instagram']
	distinct_fb_places=collection_fb.distinct('place_name')

	rslt = collection_instagram.find({"_id": {'$nin':distinct_fb_places} })
	
	return rslt


def get_place_by_mongo_id(client,database,place_id):
	client = generate_client(client)

	collection = client[database]['places']
	rslt = collection.find_one({'_id':place_id})
	
	return rslt
	



def store_hashtags_per_place_instagram(hashlist,place,instaname,instaid,client):
	if not hashlist is None and len(hashlist) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['results'] = hashlist
		to_save['place_name'] = instaname
		to_save['instagram_id']=instaid
		to_save['analysis_type']='hashtags'
		database = client['database']
		collection = 'instagram'
		save_to_database(client,database,collection,to_save)


def store_topics_per_place_instagram(topicslist,place,instaname,instaid,client):
	if not topicslist is None and len(topicslist) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['results'] = topicslist
		to_save['place_name'] = instaname
		to_save['instagram_id']=instaid
		to_save['analysis_type']='topics'
		database = client['database']
		collection = 'instagram'
		save_to_database(client,database,collection,to_save)

def store_emojis_per_place_instagram(emojilist,place,instaname,instaid,client):
	if not emojilist is None and len(emojilist) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['results'] = emojilist
		to_save['place_name'] = instaname
		to_save['instagram_id']=instaid
		to_save['analysis_type']='emojis'
		database = client['database']
		collection = 'instagram'
		save_to_database(client,database,collection,to_save)

def store_hashtags_from_captions_per_place_instagram(hashsfromcaptions,place,instaname,instaid,client):
	if not hashsfromcaptions is None and len(hashsfromcaptions) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['results'] = hashsfromcaptions
		to_save['place_name'] = instaname
		to_save['instagram_id']=instaid
		to_save['analysis_type']='hashtags_from_captions'
		database = client['database']
		collection = 'instagram'
		save_to_database(client,database,collection,to_save)

def store_topics_from_captions_per_place_instagram(topicsfromcaptions,place,instaname,instaid,client):
	if not topicsfromcaptions is None and len(topicsfromcaptions) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['results'] = topicsfromcaptions
		to_save['place_name'] = instaname
		to_save['instagram_id']=instaid
		to_save['analysis_type']='topics_from_captions'
		database = client['database']
		collection = 'instagram'
		save_to_database(client,database,collection,to_save)

def store_emojis_from_captions_per_place_instagram(emojisfromcaptions,place,instaname,instaid,client):
	if not emojisfromcaptions is None and len(emojisfromcaptions) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['results'] = emojisfromcaptions
		to_save['place_name'] = instaname
		to_save['instagram_id']=instaid
		to_save['analysis_type']='emojis_from_captions'
		database = client['database']
		collection = 'instagram'
		save_to_database(client,database,collection,to_save)

def store_ads_insight_per_place_facebook(place_ads_insights,doc,client):
	if not place_ads_insights is None and len(place_ads_insights['analysis'][0]) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = doc['place_id']
		to_save['ads_insight'] = place_ads_insights
		to_save['place_name'] = doc['place_name']

		database = client['database']
		collection = 'facebook_ads'
		save_to_database(client,database,collection,to_save)


def store_topics_twitter(twitter_topic_list,place,twittername,twitterid,client):
	if not twitter_topic_list is None and len(twitter_topic_list) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['place_name'] = twittername
		to_save['twitter_id']= twitterid
		to_save['results'] = twitter_topic_list
		to_save['analysis_type']='topics'
		database = client['database']
		collection = 'twitter'
		save_to_database(client,database,collection,to_save)


def store_emojis_twitter(twitter_emoji_list,place,twittername,twitterid,client):
	if not twitter_emoji_list is None and len(twitter_emoji_list) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['place_name'] = twittername
		to_save['twitter_id']= twitterid		
		to_save['results'] = twitter_emoji_list
		to_save['analysis_type']='emojis'
		database = client['database']
		collection = 'twitter'
		save_to_database(client,database,collection,to_save)


def store_hashtags_twitter(twitter_hashtags_list,place,twittername,twitterid,client):
	if not twitter_hashtags_list is None and len(twitter_hashtags_list) > 0:
		to_save = {}
		to_save['time'] = time.time()
		to_save['place_id'] = place['_id']
		to_save['place_name'] = twittername
		to_save['twitter_id']= twitterid
		to_save['results'] = twitter_hashtags_list
		to_save['analysis_type']='hashtags'
		database = client['database']
		collection = 'twitter'
		save_to_database(client,database,collection,to_save)


	



