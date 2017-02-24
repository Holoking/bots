from .lib import FB_functions
from .._common_lib import common_functions

from operator import itemgetter
from collections import Counter

import facebook


class hashtags_per_post_caption:

	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[hashtags_per_post_caption]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[hashtags_per_post_caption]:Missing facebook token information"

		if ('fb_post_id' in params):
			post_id = params['fb_post_id']
		else:
			return True, "[hashtags_per_post_caption]:Missing facebook post identifier"


		options={}
		# Add theoptions
		if ('threshold' in params):
			options['threshold'] = params['threshold']

		return self.Trending_hashtags_in_post_caption(graph,post_id)

	def Trending_hashtags_in_post_caption(self,FBgraph,post_id):
		booll=False
		outlistresult=[] 
		try:
			post=FBgraph.get_object(id=post_id,fields='id,message')
			caption=[{'id':post['id'],'text':post['message']}]
		except Exception as er:
			return True,str(er)
		result=common_functions.getposthashtags(caption)
		hashtaggs=Counter([hashtag
					for hashtag in result
						])
		for key in hashtaggs:
			outlistresult.append({'key':key,'count':hashtaggs[key]})   
		outlistresult=sorted(outlistresult, key=itemgetter('count'), reverse=True) 
		return False,outlistresult