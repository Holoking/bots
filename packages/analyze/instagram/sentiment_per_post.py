from .lib import Instagram_functions
from .._common_lib import common_functions

from instagram.client import InstagramAPI
import re
import json
import time
from collections import Counter


class sentiment_per_post:

	def execute(self,**params):
		"""parse the parameters"""
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[sentiment_per_post]: Missing instagram token or instagram_client_secret information"

		if ('instagram_post_id' in params):
			post_id = params['instagram_post_id']
		else:
			return True, "[sentiment_per_post]: Missing instagram post identifier"


		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[sentiment_per_post]: Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[sentiment_per_post]: Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[sentiment_per_post]: Missing microsof account_key"

		return self.sentiment_per_post(api,post_id,base_url,headers)


	def sentiment_per_post(self,api,post_id,base_url,headers):
		positivecommentsnumber=0
		negativecommentsnumber=0
		
		list_=[]
		try:
			list_=Instagram_functions.get_comment_list(api,post_id)
		except Exception as er:
			return True,str(er)
		positive,negative=common_functions.sentiment_analys_commentslist(list_,base_url,headers)
		positivecommentsnumber+=positive
		negativecommentsnumber+=negative

		listresult=[{"count": positivecommentsnumber,"key": "Positive"}, {"count": negativecommentsnumber,"key": "Negative "}]
		return False,listresult
