from instagram.client import InstagramAPI
import time


class metrics_per_post:

	def execute(self,**params):
		"""parse the parameters"""
		if ('instagram_access_token' in params) and ('instagram_client_secret' in params):
			api = InstagramAPI(access_token=params['instagram_access_token'], client_secret=params['instagram_client_secret'])
		else:
			return True, "[metrics_per_post]:  Missing instagram token or instagram_client_secret information"

		if ('instagram_post_id' in params):
			post_id = params['instagram_post_id']
		else:
			return True, "[metrics_per_post]:  Missing instagram post identifier"

		return self.metrics_per_post(api,post_id)


	def metrics_per_post(self,api,post_id):

		try:
			recent_media= api.media(post_id)
			result=[{"key":"likes","count":recent_media.like_count},{"key":"comments","count":recent_media.comment_count}]
		except Exception as er:
			return True,str(er)
			
		return False,result

