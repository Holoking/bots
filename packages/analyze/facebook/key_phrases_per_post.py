from .lib import FB_functions
from .._common_lib import common_functions

import sys
import base64
import time
import facebook
import json
import unicodedata
from operator import itemgetter
from collections import Counter


class key_phrases_per_post:

	def execute(self,**params):

		"""parse the parameters"""

		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[key_phrases_per_post]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[key_phrases_per_post]:Missing facebook token information"


		if ('fb_post_id' in params):
			post_id = params['fb_post_id']
		else:
			return True, "[key_phrases_per_post]:Missing facebook post identifier"

		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[key_phrases_per_post]:Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[key_phrases_per_post]:Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[key_phrases_per_post]:Missing microsof account_key"

		options={}
		# Add theoptions
		if ('threshold' in params):
			options['threshold'] = params['threshold']

		return self.Trending_topics_in_post_comments(graph,post_id,base_url,headers,account_key,**options)



	def Trending_topics_in_post_comments(self,FBgraph,post_id,base_url,headers,account_key,**options):
		all_list_key=[]
		listresult=[]

		commentlist,existnextcom,next_url =FB_functions.get1000comments(FBgraph,post_id)

		if len(commentlist) == 0:
			return True,next_url

		listt=common_functions.get_topic_in_commentslist(commentlist,base_url,headers)
		all_list_key.extend(listt)
		while existnextcom!=0:
			nextcomments,existnextcom,next_url=FB_functions.getnext(next_url)
			listt=common_functions.get_topic_in_commentslist(commentlist,base_url,headers)
			all_list_key.extend(listt)
		keyphrases=Counter([keyphrase 
				    for keyphrase in all_list_key
				            ])
		keyphrases=dict(keyphrases)
		for key in keyphrases:
			listresult.append({'key':key,'count':keyphrases[key]})
		booll=(len(listresult)==0)
		listresult=sorted(listresult, key=itemgetter('count'), reverse=True) 

		if 'threshold' in options:
			listresult = listresult[0:int(options['threshold'])]
		
		return False,listresult
