from .lib import Instagram_functions
from .._common_lib import common_functions


from instagram.client import InstagramAPI
import time
from operator import itemgetter
from collections import Counter


class hashtags_per_post_caption:

	def execute(self,**params):
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[hashtags_per_post_caption]: Missing instagram token or instagram_client_secret information"

		if ('instagram_post_id' in params):
			post_id = params['instagram_post_id']
		else:
			return True, "[hashtags_per_post_caption]: Missing instagram post identifier"

		return self.Trending_Hashtags_in_post_caption(api,post_id)

	def Trending_Hashtags_in_post_caption(self,api,post_id):
		booll=False
		outlistresult=[] 
		try:
			post=api.media(post_id)
			caption=[{'id':post.id,'text':post.caption.text}]
		except Exception as er:
			return True,str(er)
		result=common_functions.getposthashtags(comment_list)
		hashtaggs=Counter([hashtag
					for hashtag in result
						])
		for key in hashtaggs:
			outlistresult.append({'key':key,'count':hashtaggs[key]})   
		outlistresult=sorted(outlistresult, key=itemgetter('count'), reverse=True) 
		return False,outlistresult