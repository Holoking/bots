from instagram.client import InstagramAPI
import time

class metrics_per_page:

	def execute(self,**params):
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[followers_per_page]:  Missing instagram token or  client_secret information"

		if ('instagram_page_id' in params):
			page_id = params['instagram_page_id']
		else:
			return True, "[followers_per_page]:  Missing instagram page identifier"




		return self.get_follower_count(api,page_id)


	def get_follower_count(self,api,page_id):
		try:
			result=[]
			page = api.user(user_id=page_id)
			for key in page.counts :
				result.append({"key":key,"count":page.counts[key]})
		except Exception as er:
			return True,str(er)
		return False,result
