from .lib import Instagram_functions
from .._common_lib import common_functions


from instagram.client import InstagramAPI
import time
import datetime
from collections import Counter
from operator import itemgetter



class topics_per_page:


	def execute(self,**params):
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[topics_per_page]: Missing instagram token or  client_secret information"

		if ('instagram_page_id' in params):
			page_id = params['instagram_page_id']
		else:
			return True, "[topics_per_page]:  Missing instagram page identifier"

		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[topics_per_page]:  Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[topics_per_page]:  Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[topics_per_page]:  Missing microsof account_key"

		
		options = {}
		#Ajout des options
		if ('since' in params):
			options['since'] = params['since']
	
		if ('until' in params):
			options['until'] = params['until']

		if ('nombre' in params):
			options['nombre'] = params['nombre']

		return self.Trending_topics_in_instagram_page(api,page_id,base_url,headers,**options)


		
	def Trending_topics_in_instagram_page(self,api,page_id,base_url,headers,**option):
		result=[]
		listresult=[]
		try:
			post_list =Instagram_functions.get_post_list(api,page_id,**option) 
		except Exception as er:
			return True,str(er)

		output=[]
		for post in post_list:
			try:
				comment_list=Instagram_functions.get_comment_list(api,post['id'])
			except Exception as er:
				return True,str(er)
			listtt=common_functions.get_topic_in_positivecomments(comment_list,base_url,headers)
			if len(listtt)!=0:
				result.extend(listtt)
		keyphrases=Counter([keyphrase 
							for keyphrase in result
								])
		keyphrases=dict(keyphrases)
		for key in keyphrases:
			listresult.append({'key':key,'count':keyphrases[key]})
		listresult=sorted(listresult, key=itemgetter('count'), reverse=True) 
		return False,listresult

