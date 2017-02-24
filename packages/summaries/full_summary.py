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


def get_last_analysis(place_id,client_info):
    client = generate_client(client_info)
    return client[client_info['collection']].findOne({'place_id':place_id})



def summarize_place(place_id,source_client_info,target_client_info):
    # Get last summary in order to define the time range 
    last_analysis = get_last_analysis(place_id,target_client_info)

    try:
        since = last_analysis['time_range']['until']
    except:
        since = 0

    # Get all instagram analysis performed since 'last_analysis'
    source_client = generate_client(source_client_info)
    where = "this.time > "+ str(since)

    cursor = source_client[source_client_info['collection']].find({'place_id':place_id,"$where":where})

    time_range = {}
    try:
        time_range['from'] = last_analysis['time_range']['from']
    except:
        time_range['from'] = None
    try:
        time_range['until'] = last_analysis['time_range']['until']
    except:
        time_range['until'] = None


    target_client = generate_client(target_client_info)
    collection = client[target_client_info['database']][target_client_info['collection']]
    for analysis in cursor:
        document = get_last_analysis(place_id,target_client_info)

        if time_range['from'] is None or time_range['from'] > analysis['time']:
            time_range['from'] = analysis['time']
        if time_range['until'] is None or time_range['until'] < analysis['time']:
            time_range['until'] = analysis['time']

        try:
            finalresults = document[analysis['analysis_type']]
            for dic in analysis['results']:
                key=dic['key']
                i=0
                for f in finalresults:
                    if f['key'] == key:
                        f['count']+=dic['count']
                        break
                    else:
                        i+=1
                if i == len(finalresults):
                    finalresults.append(dic)

            collection.update_one(
            { "place_id" : doc['place_id'] },
            { '$set': {doc['analysis_type']:finalresults,'time':time.time(),'time_range':time_range}},
            upsert=True);

        except Exception as er:
            print 'Created a new document.'
            collection.update_one(
            { "place_id" : doc['place_id']},
            { '$set': {doc['analysis_type']:doc['results'],'time':time.time(),'time_range':time_range}},
            upsert= True);