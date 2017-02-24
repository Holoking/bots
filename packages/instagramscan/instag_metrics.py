from instagram.client import InstagramAPI
from datetime import datetime
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

def get_post_list(api,page_id,**option):
	epoch = datetime.utcfromtimestamp(0)
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

		if(post_epochtime>=float(sincetime) and post_epochtime<float(untiltime)):
			if (i.caption):
				text_=i.caption.text 
			else:
				text_=''
			post_list_.append({'id':i.id,'text':text_})
 

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
	return post_list_
def metrics_per_post(api,post_id):
	result=[]
	try:
		recent_media= api.media(post_id)
		result=[{"key":"likes","count":recent_media.like_count},{"key":"comments","count":recent_media.comment_count}]
	except Exception as er:
		print str(er)

	return result

def get_follower_count(api,page_id):
	result=[]
	try:
		page = api.user(user_id=page_id)
		for key in page.counts :
			result.append({"key":key,"count":page.counts[key]})
	except Exception as er:
		print str(er)
	return result


def get_user_metrics_for_the_days_of_this_week(api,page_id):
	since_=(datetime(datetime.now().year,datetime.now().month,datetime.now().day) - datetime(1970,1,1,0,0)).total_seconds()
	list_metrics=[]
	until_=since_+86400
	i=0
	while i<7:
		likes_counts=0
		comments_counts=0
		list_posts_day=get_post_list(api,10245870,since=since_,until=until_)
		  
		for b in list_posts_day:
			h=metrics_per_post(api,b['id'])
			comments_counts+=h[1]['count']
			likes_counts+=h[0]['count']
		list_metrics.append({'date':datetime.fromtimestamp(since_),'posts':len(list_posts_day),'comments':comments_counts,'likes':likes_counts})
		i+=1
		since_=since_-86400
		until_=since_+86400
	return list_metrics
def get_likes_comments_posts_week_number(api,page_id):
	likes_week_number=0
	posts_week_number=0
	comments_week_number=0
	list_week_metrics=get_user_metrics_for_the_days_of_this_week(api,page_id)
	for metric_day in list_week_metrics:
		likes_week_number+=metric_day['likes']
		posts_week_number+=metric_day['posts']
		comments_week_number+=metric_day['comments']
	output=[{'date':str(datetime.now()),'likes_over_last_week':likes_week_number,'comments_over_last_week':comments_week_number,'posts_over_last_week':posts_week_number}]
	return output

def get_list_of_average_by_day(api,page_id):
	output=[]
	list_week_metrics=get_user_metrics_for_the_days_of_this_week(api,page_id)
	for metric_day in list_week_metrics:
		if metric_day['posts']!=0:
			likes_day_average=float(metric_day['likes'])/metric_day['posts']
			comments_day_average=float(metric_day['comments'])/metric_day['posts']
		else:
			likes_day_average=0
			comments_day_average=0
		output.append({'date':metric_day['date'],'likes_day_average':likes_day_average,'comments_day_average':comments_day_average})
	return output




def Average_likes_number_per_post_over_last_week(api,page_id):
	list_week_metrics=get_likes_comments_posts_week_number(api,page_id)
	if list_week_metrics[0]['posts_over_last_week']!=0:
		return [{'Average likes number per post over last week':(float(list_week_metrics[0]['likes_over_last_week'])/list_week_metrics[0]['posts_over_last_week'])}]
	else:
		return [{'Average likes number per post over last week':0}]

def Average_comments_number_per_post_over_last_week(api,page_id):
	list_week_metrics=get_likes_comments_posts_week_number(api,page_id)
	if list_week_metrics[0]['posts_over_last_week']!=0:
		return [{'Average comments number per post over last week':(float(list_week_metrics[0]['comments_over_last_week'])/list_week_metrics[0]['posts_over_last_week'])}]
	else:
		return [{'Average comments number per post over last week':0}]

def Average_likes_number_per_day_over_last_week(api,page_id):
	list_day_average=get_list_of_average_by_day(api,page_id)
	week_per_day_average=0
	for day in list_day_average:
		week_per_day_average+=day['likes_day_average']

	return [{'Average likes number per day over last week':(float(week_per_day_average)/7)}]

def Average_comments_number_per_day_over_last_week(api,page_id):
	list_day_average=get_list_of_average_by_day(api,page_id)
	week_per_day_average=0
	for day in list_day_average:
		week_per_day_average+=day['comments_day_average']

	return [{'Average comments number per day over last week':(float(week_per_day_average)/7)}]

def engagement_by_reach(api,page_id):
	try:
		list_week_metrics=get_likes_comments_posts_week_number(api,page_id)
		engagement=list_week_metrics[0]['likes_over_last_week']+list_week_metrics[0]['comments_over_last_week']
		follower=get_follower_count(api,page_id)
		for a in follower:
			if a['key'] == 'followed_by':
				followedby=a['count']
		return [{'engagement_by_reach':(float(engagement)/followedby)}]
	except:
		return 0




