import urllib2
import urllib
import sys
import base64
import time
import facebook
import json
import requests
import unicodedata
import re
from prettytable import PrettyTable
from collections import Counter

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


def getposthashtags(listof): #listof post's comments with ids and messages
	hashindexs=[]
	hashtags=[]
	for lis in listof:
		hashindexs=[m.start() for m in re.finditer('#', lis['text'])]
		espaceindexs=[m.start() for m in re.finditer(' ', lis['text'])]            
		if len(hashindexs)!=0:
			for a in hashindexs:
				j=hashindexs.index(a)
				
				i=0
				if len(espaceindexs)==0:
					if len(hashindexs)>j+1 :
						hashtags.insert(len(hashtags),lis['text'][a:hashindexs[j+1]-len(lis['text'])])
					else:
						hashtags.insert(len(hashtags),lis['text'][a:])
																	
				for b in espaceindexs:
					if len(hashindexs)>j+1:
						if b>a and b<hashindexs[j+1] :
							hashtags.insert(len(hashtags),lis['text'][a:b-len(lis['text'])])
							break
						elif b>a and b>hashindexs[j+1]:
							hashtags.insert(len(hashtags),lis['text'][a:hashindexs[j+1]-len(lis['text'])])
							break                        
						else:
							i+=1
						if i==len(espaceindexs):
							hashtags.insert(len(hashtags),lis['text'][a:hashindexs[j+1]-len(lis['text'])])
						
					else:
						if b>a :
							hashtags.insert(len(hashtags),lis['text'][a:b-len(lis['text'])])
							break                                            
						else:
							i+=1
						if i==len(espaceindexs):                    
							hashtags.insert(len(hashtags),lis['text'][a:])

	return hashtags

	


def get_topic_in_positivecomments(comment_list,base_url,headers):
	listofkeyphrase=[]
	listresult=[]
	if len(comment_list)!=0:
		inputs=createAnalysAPIinputtext(comment_list,base_url,headers)
		if inputs !='{"documents":[]}':
			obje=sentimentanalys(base_url,inputs,headers)
			positivecommentsids=[]
			input_text=''            
			for ob in obje['documents']:
				if ob['score']>0.5:
					positivecommentsids.insert(len(positivecommentsids),ob['id'])
			for comment_sentiments in comment_list:
				textt=cleaning_text(comment_sentiments['text'])
				if comment_sentiments['id'] in positivecommentsids and comment_sentiments['id'] not in input_text and len(textt)!=0:
					input_text += '{"id":"'+comment_sentiments['id']+'","text":"'+textt+'"},'
			input_texts ='{"documents":['+input_text+']}'
			if input_texts !='{"documents":[]}':
				obje1=keyphrasesanalys(base_url,input_texts,headers)
				for ob1 in obje1['documents']:
					listofkeyphrase.extend(ob1['keyPhrases'])
	return listofkeyphrase


def sentiment_analys_commentslist(comment_list,base_url,headers):
	positivecommentsnumber=0
	negativecommentsnumber=0
	if len(comment_list)!=0:
				booll=False
				inputs=createAnalysAPIinputtext(comment_list,base_url,headers)
				if inputs!='{"documents":[]}':

					obje=sentimentanalys(base_url,inputs,headers)    
					
					for ob in obje['documents']:
						if  ob['score'] > 0.5 :
							positivecommentsnumber+=1
						else:
							negativecommentsnumber+=1
	return positivecommentsnumber,negativecommentsnumber



def get_topic_in_commentslist(commentlist,base_url,headers):
	listofkeyphrases=[]
	if len(commentlist)!=0:
		inputtextss=createAnalysAPIinputtext(commentlist,base_url,headers)
		if inputtextss!='{"documents":[]}':
			objectt=keyphrasesanalys(base_url,inputtextss,headers)
			for ob1 in objectt['documents']:
				listofkeyphrases.extend(ob1['keyPhrases'])
	return listofkeyphrases

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
