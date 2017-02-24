import urllib2
import urllib
import sys
import base64
import time
from instagram.client import InstagramAPI
import json
import requests
import unicodedata
import re
import datetime
from prettytable import PrettyTable
from collections import Counter



def get_post_list(api,page_id,**option):
	epoch = datetime.datetime.utcfromtimestamp(0)
	if 'until' in option:
		untiltime=option['until']
	else:
		untiltime=time.time()
	if 'since' in option:
		sincetime=option['since']
	else:
		sincetime=untiltime-86400    
	recent_media, next_ = api.user_recent_media(user_id=page_id)
	post_list_=[]    
	for i in recent_media:
		post_epochtime=(i.created_time-epoch).total_seconds()
 
		if(post_epochtime>float(sincetime) and post_epochtime<float(untiltime)):
			if (i.caption):
				text_=i.caption.text 
			else:
				text_=''
			print i.id
			print text_
			post_list_.append({'id':i.id,'text':text_})
			print post_list_  
		
	while(next_):
		
		recent_media, next_ = api.user_recent_media(user_id=page_id,with_next_url=next_)
		for i in recent_media:
			if(post_epochtime>float(sincetime)and post_epochtime<float(untiltime)):
				if (i.caption ):
					text_=i.caption.text
				else:
					text_=''                
				post_list_.append({'id':i.id,'text':text_})
			elif(post_epochtime<float(sincetime) ):
				return post_list_
	print post_list_
	return post_list_
def get_comment_list(api,post_id):
	comment_list_=[]
	hii=api.media_comments(post_id)
	for i in hii:
		comment_list_.append({"id": i.id,"text": i.text})
	return comment_list_