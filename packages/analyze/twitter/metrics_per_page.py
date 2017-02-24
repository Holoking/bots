import datetime
import time
import json
import tweepy

class metrics_per_page:

	def execute(self,**params):
		"""parse the parameters"""
		
		if('twitter_consumer_key' in params) and ('twitter_consumer_secret' in params) and ('twitter_access_token' in params) and ('twitter_access_token_secret' in params):
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

		return self.Get_Metrics_Timeline(profile_id = profile_id, api = api)

	### Sample ###
    # curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"get_metrics_timeline","parameters":{"twitter_profile_id":"104856942"}}' http://127.0.0.1:5000/analyze/twitter
    # twitter_profile_id = 104856942

	def Get_Metrics_Timeline(self, profile_id, api):
		redacted = False
		metrics = {}

		for page in tweepy.Cursor(api.user_timeline, user_i = profile_id).pages():
			try:	
				for status in page:
					status_id = status.id
					likes_count = status.favorite_count
					retweets_count = status.retweet_count
					metrics[status_id] = {'likes count':likes_count, 'retweets count':retweets_count}
			except Exception as exc:
				print exc
				time.sleep(60*15)
		if len(metrics) == 0:
			redacted = True
			return redacted, "Metrics Container is Empty"


		return redacted, metrics
