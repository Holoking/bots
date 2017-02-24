from .lib import FB_functions
from .._common_lib import common_functions

from operator import itemgetter
from collections import Counter

import facebook


class map_page:

	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[map_page]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[map_page]:Missing facebook token information"

		if ('fb_page_id' in params):
			page_id = params['fb_page_id']
		else:
			return True, "[map_page]:Missing facebook page identifier"

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

		if not 'date_format' in options:
			options['date_format'] = 'U'

		post_list ,existnext ,t =FB_functions.getnposts(FBgraph,page_id,'{id,created_time}',**options)

		if len(post_list) == 0:
			return True,t

		if 'threshold' in options:
			post_list = post_list[0:int(options['threshold'])]

		return False,post_list
