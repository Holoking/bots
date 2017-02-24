import datetime
import time
import json
import tweepy

class metrics_per_post:

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

        if ('twitter_post_id' in params):
            status_id = int(params['twitter_post_id'])
        else:
            return 3, "Topic Page : Missing Twitter Status Identifier"

        return self.Get_Metrics_Status(profile_id = profile_id, status_id = status_id, api = api)

    ### Sample ###
    # curl -X POST -H "Content-type: application/json" -d '{ "analysis_type": "get_metrics_status", "parameters": {"twitter_profile_id": "104856942", "twitter_post_id": "809169678568280064"}}' http://127.0.0.1:5000/analyze/twitter
    # twitter_profile_id = 104856942
    # twitter_post_id = 809169678568280064

    def Get_Metrics_Status(self, profile_id, status_id, api):
        redacted = False
        metrics = {}
        
        status_search = api.user_timeline(user_id = profile_id, max_id = status_id + 1, since_id = status_id - 1)
        for st in status_search:
            likes_count = st.favorite_count
            retweets_count = st.retweet_count
            try:
                metrics["created_time"] = str(datetime.datetime.now().strftime("%I:%M %p on %B %d, %Y"))
                metrics[str(status_id)] = {'likes count': str(likes_count), 'retweets count': str(retweets_count)}
            except Exception as exc:
                return True,str(exc)

        if len(metrics) == 0:
            redacted = True
            return redacted, "Metrics Container is Empty"
        
        return redacted, metrics