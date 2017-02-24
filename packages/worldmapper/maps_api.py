import maps_utils
import tweepy
import time

import unicodedata
import re
from collections import Counter
from operator import itemgetter


def get_states_within_country(country, gmaps):
    
    address = 'States in ' + str(country)
    states_query = gmaps.geocode(address = address)
    
    states = []
    for state in states_query:
        states.append({"Name":str(state['address_components'][0]['long_name']), "Coordinates":'(' + str(state['geometry']['location']['lat']) + ',' + str(state['geometry']['location']['lng']) + ')'})

    return states


def get_places_within_state_by_type(search_type, state, country, gmaps):

    print('searching for : '+str(search_type)+' in '+state)
   
    query = []
    next_page = True
    places = {}
    timeouts = 0
    next_pages = []

    try:
    	places = gmaps.places(query = search_type + ' in ' + state + ', ' + country, type = search_type)
    except Exception as exc:
	print('exception : '+str(type(exc).__name__)+' -> '+str(exc))

    if 'next_page_token' in places:
        next_page = places['next_page_token'].encode('utf-8')
	if next_page in next_pages:
	    print("not new next_page_token")
	else:
	    print("new next_page_token")
            next_pages.append(next_page)
    else:
    	next_page = False

    while(next_page):
    	time.sleep(3)
    	try:
            old_rslt = places['results']
            places.update(gmaps.places(query = search_type + ' in ' + state,page_token = next_page))
            places['results'].extend(old_rslt)

	    next_page = places['next_page_token'].encode('utf-8')

    	    if next_page in next_pages:
    	        places.pop('next_page_token',None)
    	    else:
    	        print("new next_page_token")
    	        next_pages.append(next_page)
    	except Exception as exc:
    	    timeouts += 1
    	    print('exception : '+str(type(exc).__name__)+' -> '+str(exc))

    	next_page = False
        if timeouts < 3 and 'next_page_token' in places:
       	    next_page = places['next_page_token'].encode('utf-8')
    	    
    
    if 'results' in places:
	    for place in places['results']:
		query.append({"formatted_address":place["formatted_address"].encode('utf-8'),"place_id":place["place_id"].encode('utf-8'),"Name":place["name"].encode('utf-8'), "lat": str(place['geometry']['location']['lat']), "lng":str(place['geometry']['location']['lng'])})
    
    print(str(len(query))+" places found.")
    return query


#def get_places_within_state_by_type(search_type, state, gmaps):    
#    query = []
#   places = gmaps.places(query = search_type + ' in ' + state, type = search_type)
#    for place in places['results']:
#        query.append({"Name":str(place["name"]), "lat": str(place['geometry']['location']['lat']), "lng":str(place['geometry']['location']['lng'])})
#    return query


def get_places_within_states(search_type,states,gmaps):
	all_places = {}
	for key in states.keys():
		print("state = "+str(key))
		state = states[key]
		try:
			all_places[state]=get_places_within_state_by_type(search_type = search_type, state = state, gmaps = gmaps)
			print("list = "+str(all_places[state]))
		except Exception as exc:
			print(exc)

	print(str(all_places))
	return all_places


def get_places_within_country_by_type(country, gmaps, search_type):
    
    states = []
    places = []
    
    states_query = get_states_within_country(country = country, gmaps = gmaps)
    for state in states_query:
        states.append({"Name":str(state['address_components'][0]['long_name']), "Coordinates":'(' + str(state['geometry']['location']['lat']) + ',' + str(state['geometry']['location']['lng']) + ')'})
    
    for state in states:
        places_query = get_places_within_state_by_type(search_type = search_type, state = str(state['Name']), gmaps = gmaps)
        for place in places_query:
            places.append({"Name":str(place['Name']), "lat":str(place['lat']), "lng":str(place['lng'])})
        
    return places


def search_places_in_Twitter(place, api):
    
    name = place['Name']
    lat = place['lat']
    lng = place['lng']
    
    count = 0
    while True:
        count += 1
        try:
            search_query = api.geo_search(query = name, lat = lat, long = lng, granularity = 'poi')
            break
        except tweepy.RateLimitError:
            if count == 4:
                count = 0
                time.sleep(60 * 15)
            else:
                count += 1

            api = maps_utils.initiate_tweepy_api()
            continue
            
    try:
        first_place = search_query[0]
        place_type = first_place.place_type
        if place_type == 'poi' or place_type == 'neighborhood': 
            place_id = first_place.id
            place_name=first_place.full_name
        else:
            return None,None
    except Exception as exc:
        return None,None
    
    return place_id,place_name


def get_tweet_text_within_place(twitter_place_id, api):
    
    tweets = []
    search_place = 'place:' + str(twitter_place_id)
    
    for page in tweepy.Cursor(api.search, q = search_place, result_type = 'Recent').pages():
        for post in page:
            try:
                tweets.append({'id':str(post.id), 'text':unicodedata.normalize('NFKD', post.text).encode('ascii','ignore')})
            except UnicodeEncodeError:
                continue
    
    return tweets


def get_hashtags_within_place(twitter_place_id, api):
    
    hashtags = {}
    search_place = 'place:' + str(twitter_place_id)

    i = 0
    for page in tweepy.Cursor(api.search, q = search_place, result_type = 'Recent').pages():
        for post in page:
            for hashtag in post.entities['hashtags']:
                try:        
                    hasht = unicodedata.normalize('NFKD', hashtag['text']).encode('ascii','ignore')
                    if i == 0:
                        hashtags = maps_utils.add_hashtag(hasht, hashtags)
                    else:
                        hashtags = maps_utils.add_hashtag(hasht)
                    i += 1
                except UnicodeEncodeError:
                    continue

    return hashtags


def get_trending_topics_within_place(twitter_place_id, base_url, headers, api):
    list_of_key_phrarses = []
    if not twitter_place_id is None:
        list_of_tweets = get_tweet_text_within_place(twitter_place_id, api)
        list_of_key_phrarses = maps_utils.whole_key_phrase_analysis_by_limit(list_text_for_sentiment = list_of_tweets, base_url = base_url, headers = headers)

    return list_of_key_phrarses


def get_trending_hashtags(twitter_place_id, api):
    trending_hashtags = []
    if not twitter_place_id is None:
        hashtags = get_hashtags_within_place(twitter_place_id, api)
        hashtags_sorted = sorted(hashtags.items(), key = itemgetter(1), reverse=True)
        for hashtag in hashtags_sorted:
            try:
                hasht = {"key": "#" + (hashtag[0]).decode('utf-8'), "count": str(hashtag[1])}
                trending_hashtags.append(hasht)
            except:
                continue
    
    return trending_hashtags


def get_trending_emojis_within_place(twitter_place_id, api):
    listemoji = []
    if  not twitter_place_id is None:
        list_of_tweets = get_tweet_text_within_place(twitter_place_id, api)

        all_=[]
        
        for q in list_of_tweets:
            try:
                # Wide UCS-4 build
                myre = re.compile(u'['                        
                    u'\U0001F300-\U0001F64F'
                    u'\u2600-\u26ff'
                    u'\U0001F680-\U0001F6FF'
                    u'\u2600-\u26FF\u2700-\u27BF]+', 
                    re.UNICODE)
            except re.error:
                # Narrow UCS-2 build
                myre = re.compile(u'('
                    u'\ud83c[\udf00-\udfff]|'
                    u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                    u'[\u2600-\u26FF\u2700-\u27BF])+', 
                    re.UNICODE)
            h=q['text']

            k=myre.findall(h)            
            while(len(k)!=0):

                for a in k:

                    l=[m.start() for m in re.finditer(a, h)]
                    for i in l:
                        all_.append(a) 
                    z=re.compile(a,re.UNICODE)
                    h=z.sub('',h)
                k=myre.findall(h)


        keyphrases=Counter([a 
                    for a in all_])
        keyphrases=dict(keyphrases)
        
        for key in keyphrases:
            listemoji.insert(len(listemoji),{'key':key,'count':keyphrases[key]})
        listemoji=sorted(listemoji, key=itemgetter('count'), reverse=True)
    
    return listemoji

