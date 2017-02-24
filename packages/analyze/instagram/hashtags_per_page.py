from .lib import Instagram_functions
from .._common_lib import common_functions


from instagram.client import InstagramAPI
import time
import datetime
from collections import Counter
from operator import itemgetter


class hashtags_per_page:

	def execute(self,**params):
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[hashtags_per_page]: Missing instagram token or  client_secret information"

		if ('instagram_page_id' in params):
			page_id = params['instagram_page_id']
		else:
			return True, "[hashtags_per_page]: Missing instagram page identifier"

		options = {}
		#Ajout des options
		if ('since' in params):
			options['since'] = params['since']
	
		if ('until' in params):
			options['until'] = params['until']

		if ('nombre' in params):
			options['nombre'] = params['nombre']

		return self.Trending_hashtags_in_instagram_page(api,page_id,**options)


	def Trending_hashtags_in_instagram_page(self,api,page_id,**option):
		outlistresult=[]
		result=[]
		try:
			post_list = Instagram_functions.get_post_list(api,page_id,**option)
		except Exception as er:
			return True,str(er)		
		for post in post_list:
			try:
				comment_list=Instagram_functions.get_comment_list(api,post['id'])
			except Exception as er:
				return True,str(er)
			listresult=common_functions.getposthashtags(comment_list)
			print listresult
			if len(listresult)!=0:
				result.extend(listresult)
		hashtaggs=Counter([hashtag
					for hashtag in result
						])
		for key in hashtaggs:
			outlistresult.insert(len(outlistresult),{'key':key,'count':hashtaggs[key]})   
		outlistresult=sorted(outlistresult, key=itemgetter('count'), reverse=True) 
		return False,outlistresult