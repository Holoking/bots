from .lib import Twitter_Analytics_Utils
from operator import itemgetter

import tweepy
import datetime
import time
import operator
import json

class key_phrases_per_page:

    def execute(self,**params):
        """parse the parameters"""
        
        if ('twitter_consumer_key' in params) and ('twitter_consumer_secret' in params) and ('twitter_access_token' in params) and ('twitter_access_token_secret' in params):
            CONSUMER_KEY = params['twitter_consumer_key']
            CONSUMER_SECRET = params['twitter_consumer_secret']
            ACCESS_TOKEN = params['twitter_access_token']
            ACCESS_TOKEN_SECRET = params['twitter_access_token_secret']
            
            auth = tweepy.OAuthHandler (CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token (ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API (auth)
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

        return self.Trending_Topics_in_Retweets_for_Twitter_Profile(start_time, end_time , profile_id, api)

    ### Sample ###
    # curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"trending_topics_in_retweets_for_profile","parameters":{"twitter_profile_id":"104856942"}}' http://127.0.0.1:5000/analyze/twitter
    # twitter_profile_id = 104856942

    def Trending_Topics_in_Retweets_for_Twitter_Profile(self, start_time, end_time , profile_id, api):
        redacted = False
        retweets_captions = []
        pattern = '%Y-%m-%d %H:%M:%S'
        for status in tweepy.Cursor(api.user_timeline, user_id = profile_id).items(200):
            created_epoch_time = int(time.mktime(time.strptime(str(status.created_at), pattern)))
            if created_epoch_time <= end_time and created_epoch_time >= start_time:
                retweets_captions.extend(Twitter_Analytics_Utils.get_retweets_captions(post_id = status.id, api = api))
        
        base_url = 'https://westus.api.cognitive.microsoft.com/'
        account_key = '5258e2016a2745dd9b3aa53f6dabc690'
        headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
        trending_topics = Twitter_Analytics_Utils.whole_key_phrase_analysis_by_limit(list_text_for_sentiment = retweets_captions, base_url = base_url, headers = headers)
        
        if len(trending_topics) == 0:
            redacted = True
            return redacted, "Trending Topics Container for Profile is Empty"
        trending_topics=sorted(trending_topics, key=itemgetter('count'), reverse=True)
        return redacted, trending_topics
