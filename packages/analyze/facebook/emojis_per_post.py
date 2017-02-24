from .lib import FB_functions
from .._common_lib import common_functions

from operator import itemgetter
from collections import Counter

import facebook

class emojis_per_post:

	def execute(self,**params):
		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[Emojis_per_post]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[Emojis_per_post]:Missing facebook token information"

		if ('fb_post_id' in params):
			post_id = params['fb_post_id']
		else:
			return True, "[Emojis_per_post]:Missing facebook post identifier"


		options={}
		# Add theoptions
		if ('threshold' in params):
			options['threshold'] = params['threshold']

		return self.Trending_Emojis_in_post_comments(graph,post_id,**options)


	def Trending_Emojis_in_post_comments(self,FBgraph,post_id,**options):
		outlistresult=[]
		listresult = []

		comment_list,existnextcom,next_ =FB_functions.get1000comments(FBgraph,post_id)
			
			
		if len(comment_list)!=0:

			Emojiss=common_functions.get_Emojis(comment_list)
			listresult.extend(Emojiss)

		else:
			return True,next_

		while existnextcom!=0:

			nextcomments,existnextcom,next_=FB_functions.getnext(next_)
			Emojiss=common_functions.get_Emojis(nextcomments)
			listresult.extend(Emojiss)


   
		outlistresult=listresult

		if 'threshold' in options:
			outlistresult = outlistresult[0:int(options['threshold'])]
		
		return False,outlistresult