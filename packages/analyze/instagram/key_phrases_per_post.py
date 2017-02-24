from .lib import Instagram_functions
from .._common_lib import common_functions
from instagram.client import InstagramAPI


import time
from collections import Counter
from operator import itemgetter




class key_phrases_per_post:

	def execute(self,**params):

		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[key_phrases_per_post]: Missing instagram token or instagram_client_secret information"

		if ('instagram_post_id' in params):
			post_id = params['instagram_post_id']
		else:
			return True, "[key_phrases_per_post]:  Missing instagram post identifier"


		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[key_phrases_per_post]:  Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[key_phrases_per_post]:  Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[key_phrases_per_post]:  Missing microsof account_key"

		return self.Trending_topics_in_post_comments(api,post_id,base_url,headers)



	def Trending_topics_in_post_comments(self,api,post_id,base_url,headers):
		listofkeyphrases=[]
		listresult=[]
		try:
			commentlist=Instagram_functions.get_comment_list(api,post_id)
		except Exception as er:
			return True,str(er)
	   
		result=common_functions.get_topic_in_commentslist(commentlist,base_url,headers)
		keyphrases=Counter([keyphrase 
							for keyphrase in result
								])
		keyphrases=dict(keyphrases)
		for key in keyphrases:
			listresult.append({'key':key,'count':keyphrases[key]})
		listresult=sorted(listresult, key=itemgetter('count'), reverse=True)
		return False,listresult   