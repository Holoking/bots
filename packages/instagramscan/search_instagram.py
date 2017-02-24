from instagram.client import InstagramAPI
import datetime
import time
from operator import itemgetter
from collections import Counter
import re
import urllib2
import urllib
import sys
import base64
import time
import json
import requests
import unicodedata
import facebook




def get_associated_keywords_instagram(api,keyword):
	list_keywords=[]
	list_keywords,next_=api.tag_search(q=keyword)
	while(next_):
		list_next_,next_=api.tag_search(q=keyword)
		list_keywords.extend(list_next_)

	return list_keywords


def search_users_by_keyword_instagram(api,keyword):
	i=0
	next_ = True
	
	while next_ :
		if i == 0:
			keyword_media,next_= api.tag_recent_media(tag_name=keyword.name)
		else:
			keyword_media,next_= api.tag_recent_media(tag_name=keyword.name,with_next_url=next_)

		for a in keyword_media:
			#page = api.user(user_id=a.user.id)
			#if page.counts['media'] >= 500 and page.counts['followed_by'] >= 10000 :
			if a.like_count >= 8000:
				list_of_infl_instagram.append({'name':a.user.full_name,'id':a.user.id})
				print 'user: %s , media likes count : %d  ' %(a.user,a.like_count)
		i+=1








