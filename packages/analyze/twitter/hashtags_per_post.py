from .lib import Twitter_Analytics_Utils
from operator import itemgetter

import tweepy
import operator

class hashtags_per_post:

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

        if ('twitter_post_id' in params):
            post_id = int(params['twitter_post_id'])
        else:
            return 2, "Topic Page : Missing Twitter Post Identifier"

        return self.Trending_Hashtags_in_Retweets_for_Twitter_Post(post_id = post_id, api = api)

    ### Sample ###
    # curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"trending_hashtags_in_retweets_for_post","parameters":{"twitter_post_id":"821630405480771585"}}' http://127.0.0.1:5000/analyze/twitter
    # twitter_post_id = 821630405480771585

    def Trending_Hashtags_in_Retweets_for_Twitter_Post(self, post_id, api):
        redacted = False
        hashtags = {}
        
        hashtags = Twitter_Analytics_Utils.get_retweets_hashtags(post_id = post_id, api = api, hashtags = hashtags)
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
            return redacted, "Trending Hashtags Container in Post is Empty"
        trending_hashtags=sorted(trending_hashtags, key=itemgetter('count'), reverse=True)
        return redacted, trending_hashtags
