import googlemaps
import time


def initiate_google_maps_api(gmkey):
    
    google_maps = googlemaps.Client(key= gmkey)

    return google_maps



def get_places_within_state_by_type(search_type, state, country, gmaps):

    print('searching for : '+str(search_type)+' in '+state)    
    query = []
    next_page = True
    try:
    	places = gmaps.places(query = search_type + ' in ' + state + ', ' + country, type = search_type)
    except Exception as exc:
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(exc)
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(1)
    	print(1)

    if 'next_page_token' in places:
        next_page = places['next_page_token'].encode('utf-8')
    else:
    	next_page = False

    while(next_page):
    	time.sleep(3)
    	places = []
    	try:
            places = gmaps.places(query = search_type + ' in ' + state, type = search_type,page_token = next_page)
    	except Exception as exc:
    	    print(exc)

        if 'next_page_token' in places:
       	    next_page = places['next_page_token'].encode('utf-8')
    	else:
    	    next_page = False
    	    
    for place in places['results']:
    	print(place)
        query.append({"formatted_address":place["formatted_address"].encode('utf-8'),"place_id":place["place_id"].encode('utf-8'),"Name":place["name"].encode('utf-8'), "lat": str(place['geometry']['location']['lat']), "lng":str(place['geometry']['location']['lng'])})
    
    return query
