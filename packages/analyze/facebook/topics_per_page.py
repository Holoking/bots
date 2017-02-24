from .lib import FB_functions
from .._common_lib import common_functions

import sys
import base64
import time
import facebook
import json

from operator import itemgetter
from collections import Counter



class topics_per_page:


	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[hashtags_per_page]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[topics_per_page]:Missing facebook token information"

		if ('fb_page_id' in params):
			page_id = params['fb_page_id']
		else:
			return True, "[topics_per_page]:Missing facebook page identifier"

		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[topics_per_page]:Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[topics_per_page]:Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[topics_per_page]:Missing microsof account_key"

		
		options = {}
		#Ajout des options
		if ('since' in params):
			options['since'] = params['since']
	
		if ('until' in params):
			options['until'] = params['until']

		if ('limit' in params):
			options['nombre'] = params['limit']
	
		if ('threshold' in params):
			options['threshold'] = params['threshold']

		return self.Trending_topics_in_fb_page(graph,page_id,base_url,headers,**options)


		
	def Trending_topics_in_fb_page(self,FBgraph,page_id,base_url,headers,**options):
		all_list_key=[]
		listresult=[]

		post_list ,existnext ,t =FB_functions.getnposts(FBgraph,page_id,**options)    
		output=[]

		if len(post_list) == 0:
			return True,t

		for post in post_list:
			commentlist,existnextcom,next_url =FB_functions.get1000comments(FBgraph,post['id'])
			if len(commentlist) == 0:
				return True,next_url

			listt=common_functions.get_topic_in_positivecomments(commentlist,base_url,headers)
			all_list_key.extend(listt)

			while existnextcom!=0:

				nextcomments,existnextcom,next_url=FB_functions.getnext(next_url)
				listt=common_functions.get_topic_in_positivecomments(commentlist,base_url,headers)
				all_list_key.extend(listt)

		keyphrases=Counter([keyphrase 
							for keyphrase in all_list_key
								 ])
		keyphrases=dict(keyphrases)
		for key in keyphrases:
			listresult.append({'key':key,'count':keyphrases[key]})
		listresult=sorted(listresult, key=itemgetter('count'), reverse=True) 
	
		if 'threshold' in options:
			listresult = listresult[0:int(options['threshold'])]

		return False,listresult
