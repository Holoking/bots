from .lib import Twitter_Analytics_Utils
from operator import itemgetter
from .._common_lib import common_functions
import re
from prettytable import PrettyTable
from collections import Counter
from operator import itemgetter
import tweepy
import operator

class key_phrases_per_post_caption:

	def execute(self,**params):
		"""parse the parameters"""
		
		if ('twitter_consumer_key' in params) and ('twitter_consumer_secret' in params) and ('twitter_access_token' in params) and ('twitter_access_token_secret' in params):
			CONSUMER_KEY = params['twitter_consumer_key']
			CONSUMER_SECRET = params['twitter_consumer_secret']
			ACCESS_TOKEN = params['twitter_access_token']
			ACCESS_TOKEN_SECRET = params['twitter_access_token_secret']
			
			auth = tweepy.OAuthHandler (CONSUMER_KEY, CONSUMER_SECRET)
			auth.set_access_token (ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
			api = tweepy.API (auth,wait_on_rate_limit=True)
		else:
			return 1, "Topic Page : Missing Twitter token information"

		if ('twitter_post_id' in params):
			post_id = int(params['twitter_post_id'])
		else:
			return 2, "Topic Page : Missing Twitter Post Identifier"

		return self.Trending_topics_in_for_Twitter_Post_txt(post_id = post_id, api = api)

	### Sample ###
	# curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"trending_hashtags_in_retweets_for_post","parameters":{"twitter_post_id":"821630405480771585"}}' http://127.0.0.1:5000/analyze/twitter
	# twitter_post_id = 821630405480771585

	def Trending_topics_in_for_Twitter_Post_txt(self, post_id, api):
		booll=False
		listresult=[] 
		base_url = 'https://westus.api.cognitive.microsoft.com/'
		account_key = '5258e2016a2745dd9b3aa53f6dabc690'
		headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
		try:
			caption=Twitter_Analytics_Utils.get_post_text(post_id,api)
		except Exception as er:
			return True,str(er)
		result=common_functions.get_topic_in_commentslist(caption,base_url,headers)
		keyphrases=Counter([keyphrase 
							for keyphrase in result
								])
		keyphrases=dict(keyphrases)
		for key in keyphrases:
			listresult.append({'key':key,'count':keyphrases[key]})
		listresult=sorted(listresult, key=itemgetter('count'), reverse=True)
		return False,listresult