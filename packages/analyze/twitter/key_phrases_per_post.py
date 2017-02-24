from .lib import Twitter_Analytics_Utils
from operator import itemgetter
import tweepy

class key_phrases_per_post:

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

		return self.Trending_Topics_in_Retweets_for_Twitter_Post(post_id = post_id, api = api)

	### Sample ###
	# curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"trending_topics_in_retweets_for_post","parameters":{"twitter_post_id":"786440157452840960"}}' http://127.0.0.1:5000/analyze/twitter
	# twitter_post_id = 786440157452840960

	def Trending_Topics_in_Retweets_for_Twitter_Post(self, post_id, api):
		redacted = False
		retweets_captions = []
		retweets_captions = Twitter_Analytics_Utils.get_retweets_captions(post_id = post_id, api = api)

		base_url = 'https://westus.api.cognitive.microsoft.com/'
		account_key = '5258e2016a2745dd9b3aa53f6dabc690'
		headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
		list_of_key_phrarses = Twitter_Analytics_Utils.whole_key_phrase_analysis_by_limit(list_text_for_sentiment = retweets_captions, base_url = base_url, headers = headers)
		
		if len(list_of_key_phrarses) == 0:
			redacted = True
			return redacted, "Trending Topics Container for Post is Empty"
		list_of_key_phrarses=sorted(list_of_key_phrarses, key=itemgetter('count'), reverse=True)
		return redacted, list_of_key_phrarses
