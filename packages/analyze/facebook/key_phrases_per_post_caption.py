from .lib import FB_functions
from .._common_lib import common_functions

from operator import itemgetter
from collections import Counter

import facebook


class key_phrases_per_post_caption:

	def execute(self,**params):
		"""parse the parameters"""

		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[key_phrases_per_post]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[key_phrases_per_post]:Missing facebook token information"


		if ('fb_post_id' in params):
			post_id = params['fb_post_id']
		else:
			return True, "[key_phrases_per_post]:Missing facebook post identifier"

		if ('microsoft_base_url' in params):
			base_url = params['microsoft_base_url']
		else:
			return True, "[key_phrases_per_post]:Missing microsoft base url"

		if ('microsoft_required_headers' in params):
			headers = params['microsoft_required_headers']
		else:
			return True, "[key_phrases_per_post]:Missing microsof required headers"

		if ('microsoft_account_key' in params):
			account_key = params['microsoft_account_key']
		else:
			return True, "[key_phrases_per_post]:Missing microsof account_key"

		options={}
		# Add theoptions
		if ('threshold' in params):
			options['threshold'] = params['threshold']
		return self.Trending_topics_in_post_caption(graph,post_id,base_url,headers)

	def Trending_topics_in_post_caption(self,FBgraph,post_id,base_url,headers):
		booll=False
		listresult=[] 
		try:
			post=FBgraph.get_object(id=post_id,fields='id,message')
			caption=[{'id':post['id'],'text':post['message']}]
		except Exception as er:
			return True,str(er)
		result=common_functions.get_topic_in_commentslist(caption,base_url,headers)
		keyphrases=Counter([keyphrase 
							for keyphrase in result
								])
		keyphrases=dict(keyphrases)
		for key in keyphrases:
			listresult.append({'key':key,'count':keyphrases[key]})
		listresult=sorted(listresult, key=itemgetter('count'), reverse=True)
		return False,listresult