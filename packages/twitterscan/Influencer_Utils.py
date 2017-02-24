import tweepy
import time
import operator


def initiate_tweepy_api():
    
    CONSUMER_KEY = 'Qge555cNrzEam8Jg8sFpab0Kd'
    CONSUMER_SECRET = 'PlV17teVMVReIdmpeC83CvObDqbCm2BpaQpLlJDRmfUesrthGD'
    ACCESS_TOKEN = '2270386158-gcG5jdmxIXVV4VVPNeNRAzYBgOUsMqzNkIiwsz4'
    ACCESS_TOKEN_SECRET = 'dzvIqd2tjDRyjNagPcFh3FtlwghOGREPF4qpH1BcByCBz'

    auth = tweepy.OAuthHandler (CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token (ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API (auth)
    
    return api


def add_hashtag(hashtag, hashtags):
    
    if hashtag in hashtags:
        hashtags[hashtag] = hashtags[hashtag] + 1
    else:
        hashtags[hashtag] = 1
    
    return hashtags


def get_user(user_id, api):
    
    user = api.get_user(user_id = user_id)
    
    return user


def get_user_timeline(user_id, api):
    
    pattern = '%Y-%m-%d %H:%M:%S'
    user_statuses = []
    statuses_query = tweepy.Cursor(api.user_timeline, id = user_id, since_id = 821535793185329150).items()
    for status in statuses_query:
        user_statuses.append(status)
    
    return user_statuses


def get_metrics_history(user_id, api, period):
    
    likes_data = {}
    retweets_data = {}
    pattern = '%Y-%m-%d %H:%M:%S'
    
    user_statuses = []
    query_count = int(10)
    check = True
    time_now = int(time.time())
    max_time = time_now - period

    statuses_query = tweepy.Cursor(api.user_timeline, id = user_id).items(query_count)
    
    while(check):
        for status in statuses_query:
            max_id = str(status.id_str)
            created_epoch_time = int(time.mktime(time.strptime(str(status.created_at), pattern)))
            if created_epoch_time >=  max_time:
                likes_data[created_epoch_time] = status.favorite_count
                retweets_data[created_epoch_time] = status.retweet_count
            else:
                check = False
                continue
        statuses_query = tweepy.Cursor(api.user_timeline, id = user_id, max_id = int(max_id) - int(1)).items(query_count)

    likes_data_sorted = sorted(likes_data.items(), key=operator.itemgetter(0))
    retweets_data_sorted = sorted(retweets_data.items(), key=operator.itemgetter(0))
    
    return likes_data_sorted, retweets_data_sorted


def calculate_average_by_day(timestamp, data):
    
    output = {}
    
    a, b = data[0]
    t_min = t = a
    a, b = data[len(data) - 1]
    t_max = a
    
    index = 0
    somme = 0
    day_number = 0
    while(t < t_max):
        t_margin = min(t + timestamp, t_max)
        day_number = day_number + 1
        a, b = data[index]
        
        posts_count = 0
        posts_likes_per_day = 0
        while index < len(data) and t_margin > a:
            posts_count = posts_count + 1
            posts_likes_per_day = posts_likes_per_day + b
            index = index + 1
            a, b = data[index]
        
        try:
            output[str(day_number)] = (posts_likes_per_day / posts_count)
        except Exception as exc:
            output[str(day_number)] = 0
        
        t = t_margin
    return output
