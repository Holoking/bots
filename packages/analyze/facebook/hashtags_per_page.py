from .lib import FB_functions
from .._common_lib import common_functions

from operator import itemgetter
from collections import Counter

import facebook


class hashtags_per_page:

	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[hashtags_per_page]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[hashtags_per_page]:Missing facebook token information"

		if ('fb_page_id' in params):
			page_id = params['fb_page_id']
		else:
			return True, "[hashtags_per_page]:Missing facebook page identifier"

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

		return self.Trending_hashtags_in_facebook_page(graph,page_id,**options)


	def Trending_hashtags_in_facebook_page(self,FBgraph,page_id,**options):

		listresult=[]
		outlistresult=[]

		post_list ,existnext ,t =FB_functions.getnposts(FBgraph,page_id,**options)

		if len(post_list) == 0:
			return True,t

		for post in post_list:

			
			comment_list,existnextcom,next_ =FB_functions.get1000comments(FBgraph,post['id'])
			
			
			if len(comment_list)!=0:

				hashtagss=common_functions.getposthashtags(comment_list)
				listresult.extend(hashtagss)

			else:
				return True,next_

			while existnextcom!=0:

				nextcomments,existnextcom,next_=FB_functions.getnext(next_)
				hashtagss=common_functions.getposthashtags(nextcomments)
				listresult.extend(hashtagss)
			
		hashtaggs=Counter([hashtag
						for hashtag in listresult
							 ])
		for key in hashtaggs:
			outlistresult.append({'key':key,'count':hashtaggs[key]})  

		outlistresult=sorted(outlistresult, key=itemgetter('count'), reverse=True)

		if 'threshold' in options:
			outlistresult = outlistresult[0:int(options['threshold'])]

		return False,outlistresult
