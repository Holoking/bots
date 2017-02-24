import urllib2
import urllib
import sys
import base64
import time
import json
import requests
import unicodedata
import re
from prettytable import PrettyTable
from collections import Counter
from operator import itemgetter


def cleaning_text(text_):
	textout=text_.encode('ascii', 'replace').replace('\r',' ').replace('\\','').replace('"',' ').replace('\n',' ').replace("'"," ").replace('?','').replace('https//','')
	return textout


def createAnalysAPIinputtext(listofmax1000,base_url,headers):  #max(len(input)) for microsoftapi = 1000
	input_text=''
	input_text1=''
	for l in listofmax1000:
		text=cleaning_text(l['text'])
		if len(text)!=0 and l['id'] not in input_text :
			input_text += '{"id":"'+l['id']+'","text":"'+text+'"},'
	input_texts ='{"documents":['+input_text+']}'
	if input_texts!='{"documents":[]}':
		objj=languageanalys(base_url,input_texts,headers)
		input_text1=''
		for l in listofmax1000:
			text1=cleaning_text(l['text'])
			for ob in objj['documents'] :
				if ob['id']==l['id'] and l['id'] not in input_text1 and len(text1)!=0:
					if ob['detectedLanguages'][0]['name']=='English' or ob['detectedLanguages'][0]['name']=='French':
						input_text1 += '{"id":"'+l['id']+'","text":"'+text1+'"},'
	input_texts1 ='{"documents":['+input_text1+']}'
					
	return input_texts1


def languageanalys(base_url,input_texts,headers):
	num_detect_langs=1
	language_detection_url = base_url + 'text/analytics/v2.0/languages' + ('?numberOfLanguagesToDetect=' + num_detect_langs if num_detect_langs > 1 else '')
	req = urllib2.Request(language_detection_url, input_texts, headers)
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)
	return obj


def sentimentanalys(base_url,input_texts,headers):
	batch_sentiment_url = base_url +'text/analytics/v2.0/sentiment'
	req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)
	return obj


def keyphrasesanalys(base_url,input_texts,headers):
	batch_sentiment_url = base_url +'text/analytics/v2.0/keyPhrases'
	req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
	response = urllib2.urlopen(req)
	result = response.read()
	obj = json.loads(result)
	return obj


def get_topics_place_comments(comment_list,base_url,headers):
	result=[]
	minn=0
	i=1000
	maxx=0
	while maxx<len(comment_list):
		maxx=min(i,len(comment_list))
		print minn
		print maxx
		h=comment_list[minn:maxx]

		listt=get_topic_in_commentslist(h,base_url,headers)


		result.extend(listt)
		minn=maxx
		i+=1000
	keyphrases=Counter([keyphrase 
						for keyphrase in result ])
	keyphrases=dict(keyphrases)
	listresult=[]
	for key in keyphrases:
		listresult.append({'key':key,'count':keyphrases[key]})

	listresult=sorted(listresult, key=itemgetter('count'), reverse=True)
	return listresult


def get_Emojis(list_):
	all_=[]
	for q in list_:
		try:
		# Wide UCS-4 build
			myre = re.compile(u'['                        
				u'\U0001F300-\U0001F64F'
				u'\u2600-\u26ff'
				u'\U0001F680-\U0001F6FF'
				u'\u2600-\u26FF\u2700-\u27BF]+', 
				re.UNICODE)
		except re.error:
		# Narrow UCS-2 build
			myre = re.compile(u'('
				u'\ud83c[\udf00-\udfff]|'
				u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
				u'[\u2600-\u26FF\u2700-\u27BF])+', 
				re.UNICODE)
		h=q['text']

		k=myre.findall(h)            
		while(len(k)!=0):

			for a in k:

				l=[m.start() for m in re.finditer(a, h)]
				for i in l:
					all_.append(a) 
				z=re.compile(a,re.UNICODE)
				h=z.sub('',h)
			k=myre.findall(h)


	keyphrases=Counter([a 
				for a in all_])
	keyphrases=dict(keyphrases)
	listemoji=[]
	for key in keyphrases:
		listemoji.insert(len(listemoji),{'key':key,'count':keyphrases[key]})
	listemoji=sorted(listemoji, key=itemgetter('count'), reverse=True)
	return listemoji


def get_topic_in_commentslist(commentlist,base_url,headers):
	listofkeyphrases=[]
	if len(commentlist)!=0:
		inputtextss=createAnalysAPIinputtext(commentlist,base_url,headers)
		if inputtextss != '{"documents":[]}':
			objectt=keyphrasesanalys(base_url,inputtextss,headers)
			for ob1 in objectt['documents']:
				listofkeyphrases.extend(ob1['keyPhrases'])
	return listofkeyphrases


def get_place_id(api,place):
	try:
		print(str(place))
		h=api.location_search(q=place['Name'],count=1, lat=place['lat'], lng=place['lng'])
		print(str(h[0].id))
	except Exception as exc:
		print(str(exc))
		return None,None

	print(h[0])
	if h[0].id == "0":
		print(h[0])
		return None,None

	return h[0].id,h[0].name
