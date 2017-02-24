from .lib import FB_functions
from .._common_lib import common_functions

from operator import itemgetter
from collections import Counter

import facebook


class metrics_per_page:

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



		return self.Metricss_in_facebook_page(graph,page_id)


	def Metricss_in_facebook_page(self,FBgraph,page_id):
		try:
	    	count=FBgrah.get_object(id=page_id,fields='engagement,fan_count,checkins,talking_about_count')
	    	output =[{'count': count['engagement']['count'], 'key': 'engagement'},{'count': count['fan_count'], 'key': 'fan_count'},{'count': count['checkins'], 'key': 'checkins'},{'count': count['talking_about_count'], 'key': 'talking_about_count'}]
	    	outlistresult=output
	    except Exception as er:
	    	return True,str(er)

		return False,outlistresult
