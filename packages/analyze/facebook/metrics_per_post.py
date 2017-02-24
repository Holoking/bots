import sys
import base64
import time
import facebook
import json
import requests
import unicodedata


class metrics_per_post:

	def execute(self,**params):

		"""parse the parameters"""
		if ('fb_access_token' in params) and ('fb_token_version' in params):
			try:
				graph = facebook.GraphAPI(access_token=params['fb_access_token'],version=params['fb_token_version'])
			except:
				return True, "[metrics_per_post]:Error while accessing Facebook GraphAPI"
		else:
			return True, "[metrics_per_post]:Missing facebook token information"

		if ('fb_post_id' in params):
			post_id = params['fb_post_id']
		else:
			return True, "[metrics_per_post]:Missing facebook page identifier"

		return self.metrics_per_post(graph,post_id)


	def metrics_per_post(self,FBgrah,post_id):

		try :
			metric=FBgrah.get_object(id=post_id,fields='shares,comments.limit(0).summary(True),reactions.type(LIKE).limit(0).summary(true).as(like),reactions.type(LOVE).limit(0).summary(true).as(love),reactions.type(WOW).limit(0).summary(true).as(wow),reactions.type(HAHA).limit(0).summary(true).as(haha),reactions.type(SAD).limit(0).summary(true).as(sad),reactions.type(ANGRY).limit(0).summary(true).as(angry), reactions.type(THANKFUL).limit(0).summary(true).as(thankful)')
		except Exception as exc:
			return True,str(exc)

		result=[{"key":"like","count":metric['like']['summary']['total_count']},{"key":"love","count":metric['love']['summary']['total_count']},{"key":"wow","count":metric['wow']['summary']['total_count']},{"key":"haha","count":metric['haha']['summary']['total_count'] },{"key":"sad","count":metric['sad']['summary']['total_count'] },{"key":"angry","count":metric['angry']['summary']['total_count'] },{"key":"thankful","count":metric['thankful']['summary']['total_count'] },{"key":"shares","count":metric['shares']['count']},{"key":"comment","count":metric['comments']['summary']['total_count']}]
		
		return False,result 
