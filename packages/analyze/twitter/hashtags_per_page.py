from .lib import Twitter_Analytics_Utils
from operator import itemgetter

import tweepy
import operator
import time
import datetime

class hashtags_per_page:

    def execute(self,**params):
        """parse the parameters"""
        
        if ('twitter_consumer_key' in params) and ('twitter_consumer_secret' in params) and ('twitter_access_token' in params) and ('twitter_access_token_secret' in params):
            CONSUMER_KEY = params['twitter_consumer_key']
            CONSUMER_SECRET = params['twitter_consumer_secret']
            ACCESS_TOKEN = params['twitter_access_token']
            ACCESS_TOKEN_SECRET = params['twitter_access_token_secret']
        else:
            return 1, "Topic Page : Missing Twitter token information"

        if ('twitter_profile_id' in params):
            profile_id = int(params['twitter_profile_id'])
        else:
            return 2, "Topic Page : Missing Twitter Profile Identifier"

        if ('until' in params):
            end_time = int(params['until'])
        else:
            time_now = int (time.time())
            end_time = time_now
            
        if ('since' in params): 
            if int(params['since']) < end_time:
                start_time = int(params['since'])
        else:
            start_time = end_time - 86400
            
        auth = tweepy.OAuthHandler (CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token (ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API (auth)

        return self.Trending_Hashtags_in_Retweets_for_Twitter_Profile(start_time = start_time, end_time = end_time, profile_id = profile_id, api = api)

    ### Sample ###
    # curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"trending_hashtags_in_retweets_for_profile","parameters":{"twitter_profile_id":"104856942", "since": "1484151355" , "until": "1484756155"}}' http://127.0.0.1:5000/analyze/twitter
    # twitter_profile_id = 104856942
    # since = 1484151355
    # until = 1484756155

    def Trending_Hashtags_in_Retweets_for_Twitter_Profile(self, start_time, end_time, profile_id, api):
        redacted = False
        hashtags = {}
        pattern = '%Y-%m-%d %H:%M:%S'
        
        for status in tweepy.Cursor(api.user_timeline, user_id = profile_id).items(200):
            created_epoch_time = int(time.mktime(time.strptime(str(status.created_at), pattern)))
            if created_epoch_time <= end_time and created_epoch_time >= start_time:
                hashtag = Twitter_Analytics_Utils.get_retweets_hashtags(post_id = status.id_str, api = api, hashtags = hashtags)
                hashtags.update(hashtag)
        
        hashtags_sorted = sorted(hashtags.items(), key=operator.itemgetter(1), reverse=True)
        trending_hashtags = []
        for hashtag in hashtags_sorted:
            try:
                hasht = {"hashtag ": "#" + (hashtag[0]).decode('utf-8'), "count ": str(hashtag[1])}
                trending_hashtags.append(hasht)
            except Exception as exc:
                print (exc)
                continue

        if len(trending_hashtags) == 0:
            redacted = True
            return redacted, "Trending Hashtags Container in Profile is Empty"
        trending_hashtags=sorted(trending_hashtags, key=itemgetter('count'), reverse=True)
        return redacted, trending_hashtags
