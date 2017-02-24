from .lib import FB_functions
from .._common_lib import common_functions


import sys
import base64
import time
import facebook
import json
import requests
from prettytable import PrettyTable
from collections import Counter



class sentiment_per_post:

	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[sentiment_per_post]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[sentiment_per_post]:Missing facebook token information"

		if ('fb_post_id' in params):
			post_id = params['fb_post_id']
		else:
			return True, "[sentiment_per_post]:Missing facebook post identifier"

		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[sentiment_per_post]:Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[sentiment_per_post]:Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[sentiment_per_post]:Missing microsof account_key"

		return self.sentiment_per_post(graph,post_id,base_url,headers)


	def sentiment_per_post(self,FBgraph,post_id,base_url,headers):

		positivecommentsnumber=0
		negativecommentsnumber=0

		comment_list ,existnext ,next_=FB_functions.get1000comments(FBgraph,post_id)

		if len(comment_list)==0:
			return True,next_

		positive,negative=common_functions.sentiment_analys_commentslist(comment_list,base_url,headers)
		positivecommentsnumber+=positive
		negativecommentsnumber+=negative

		while existnext != 0 :
			nextcomm,existnext,next_=FB_functions.getnext(next_)
			positive,negative=common_functions.sentiment_analys_commentslist(nextcomm,base_url,headers)
			positivecommentsnumber+=positive
			negativecommentsnumber+=negative
			
		listresult=[{"count": positivecommentsnumber,"key": "Positive"}, {"count": negativecommentsnumber,"key": "Negative "}]

		return False,listresult 
		        
	    
