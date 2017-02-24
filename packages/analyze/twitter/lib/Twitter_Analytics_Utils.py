import tweepy
import json
import time
import datetime
import os
import operator
import urllib2
from collections import Counter
from ..._common_lib import common_functions

def add_hashtag(hashtag, hashtags):
	if hashtag in hashtags:
		hashtags[hashtag] = hashtags[hashtag] + 1
	else:
		hashtags[hashtag] = 1
	return hashtags

def add_retweeter(user_id, retweeters):
	if user_id in retweeters.keys():
		retweeters[user_id] = retweeters[user_id] + 1
	else:
		retweeters[user_id] = 1
	return retweeters

def create_analysis_API_input_text(listofmax1000):
	input_text = ''
	for l in listofmax1000:
		if len(l['text'])!=0 and l['id'] not in input_text:
			input_text += '{"id":"'+l['id']+'","text":"'+l['text'].encode('ascii', 'replace').replace('"',' ').replace('/',' ').replace('\n',' ').replace("'"," ")+'"},'
	input_texts = '{"documents":['+ input_text +']}'
	return input_texts

def get_retweeters_statuses(api, retweeter_ids, start_time, end_time, list_text_for_sentiment):
	pattern = '%Y-%m-%d %H:%M:%S'
		
	j = 0
	for retweeter in retweeter_ids:
		rtw_id = retweeter[0]
		i = 0
		for user_status in tweepy.Cursor(api.user_timeline, user_id = rtw_id, count = 240).items():
			i = i + 1
			created_epoch_time = int(time.mktime(time.strptime(str(user_status.created_at), pattern)))
			if created_epoch_time <= end_time and created_epoch_time >= start_time:
				status_text = handle_account_name(user_status.text)
				status_text2 = handle_https(status_text)
				list_text_for_sentiment.append({'id':str(user_status.id) , 'text' : status_text2 })
		print 'statuses count = %d' %i
		j = j + 1
	print 'all count = %d' %j
	return list_text_for_sentiment

def get_retweets_captions(post_id, api):
	captions = []
	query = api.search(q = post_id, count = 100, result_type = 'Mixed', included_entities = False)
	
	for status in query:
		try:
			quoted_status = str(status.is_quote_status)
			original_status_id = str(status.quoted_status_id_str)
			if quoted_status == 'True' and original_status_id == str(post_id):
				caption = handle_https(status.text)
				captions.append({'id':str(status.id_str) , 'text' : str(caption) } )
				#Only english captions are appended to "captions" list !!
		except Exception:
			continue
	return captions

def get_retweets_hashtags(post_id, api, hashtags):
	query = api.search(q = post_id, count = 100, result_type = 'Recent', included_entities = True)
	for status in query:
		try:
			quoted_status = str(status.is_quote_status)
			original_status_id = str(status.quoted_status_id_str)
			if quoted_status == 'True' and original_status_id == str(post_id):
				status_hashtags = status.entities['hashtags']
				
				for hashtag in status_hashtags:
					hashtags = add_hashtag(hashtag['text'], hashtags)
		
		except Exception:
			continue
	return hashtags

def handle_account_name(status):
	try:
		index = status.find(':')
		if index != -1:
			status_text = status[index + 1:]
			return status_text
	except Exception as e:
		print 'HANDLE HTTPS FUNCTION EXCEPTION'
		print 'Exception message : '
		print e
		return status
	return status

def handle_https(status):
	https_index = status.find('https')
	part1 = status
	part2 = ''
	try:
		while https_index != -1:
			part1 = status[:https_index - 1]
			rest_part = status[https_index:]
			space_index = rest_part.find(' ')
			if space_index != -1:
				part2 = rest_part[space_index:]
			else:
				part2 = ''
			status = part1 + part2
			https_index = status.find('https')
	except Exception as e:
		print 'HANDLE HTTPS FUNCTION EXCEPTION'
		print 'Exception message : '
		print e
		return status
	
	return part1 + part2

def keyphrase_analysis(input_texts, base_url, headers):
	batch_sentiment_url = base_url +'text/analytics/v2.0/keyPhrases'
	req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)
	return obj

def sentiment_analysis(input_texts, base_url, headers):
	batch_sentiment_url = base_url +'text/analytics/v2.0/sentiment'
	req = urllib2.Request(batch_sentiment_url, input_texts, headers)
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)
	return obj

def whole_key_phrase_analysis(list_text_for_sentiment, base_url, headers):
	input_text1=''
	input_texts1=''
	input_text=''
	input_texts=''
	listofkeyphrase=[]
	listresult = []
	i = 1
	for text_for_sentiment in list_text_for_sentiment:
		print i
		i = i + 1
		if len(text_for_sentiment['text'])!=0:
			var_text = str(text_for_sentiment['text'].encode('ascii', 'replace').replace('"',' ').replace('/',' ').replace('\n',' ').replace("'"," ").replace("?",""))
			if len(var_text) != 0:
				input_text += '{"id":"'+ str(text_for_sentiment['id'])+'","text":var_text}'
			else:
				continue
		input_texts ='{"documents":['+input_text+']}'
		batch_sentiment_url = base_url +'text/analytics/v2.0/keyPhrases'
		try:
			req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
			response = urllib2.urlopen(req)
			result = response.read()
			obj = json.loads(result)
			for ob in obj['documents']:
				listofkeyphrase.extend(ob['keyPhrases'])

			keyphrases=Counter([keyphrase 
					for keyphrase in listofkeyphrase])
			keyphrases=dict(keyphrases)
			for key in keyphrases:
				listresult.append({'key':key,'count':keyphrases[key]})

		except urllib2.HTTPError as httpErr:
			print (httpErr)
			print ('http error : keyphrase_analysis')
			continue
	return listresult

def whole_key_phrase_analysis_by_limit(list_text_for_sentiment, base_url, headers):
	input_text1=''
	input_texts1=''
	input_text=''
	input_texts=''
	listofkeyphrase=[]
	listresult = []
	i = 1

	list_text_for_sentiment = list_text_for_sentiment[:1200]
	length = len(list_text_for_sentiment)
	count = 0
	while(count * 1000 < length):
		list_by_limit = list_text_for_sentiment[count * 1000:min((count + 1) * 1000, length)]
		input_text = common_functions.createAnalysAPIinputtext(list_by_limit, base_url, headers)
		obj = common_functions.keyphrasesanalys(base_url,input_text,headers)
		count = count + 1

		for ob in obj['documents']:
			listofkeyphrase.extend(ob['keyPhrases'])
			
	keyphrases = Counter([keyphrase 
					for keyphrase in listofkeyphrase])
	keyphrases=dict(keyphrases)
	for key in keyphrases:
		listresult.append({'key':key,'count':keyphrases[key]})        

	return listresult
