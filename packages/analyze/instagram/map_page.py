from instagram.client import InstagramAPI
from .lib import Instagram_functions
import time

class map_page:

	def execute(self,**params):
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[map_page]:  Missing instagram token or  client_secret information"

		if ('instagram_page_id' in params):
			page_id = params['instagram_page_id']
		else:
			return True, "[map_page]:  Missing instagram page identifier"

		return self.map_page(api,page_id,**params)


	def map_page(self,api,page_id,**options):
		result=[]
		try:
			rslt = Instagram_functions.get_post_list(api,page_id,**options)
			for r in rslt:
				result.append(r['id'])
		except Exception as er:
			return True,str(er)
		return False,result
