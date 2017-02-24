from instagram.client import InstagramAPI
import datetime
import time

from operator import itemgetter
from collections import Counter
import re

def trending_hashtags_place_comments(comment_list):
	listt2=getposthashtags(comment_list)
	keyphrases2=Counter([keyphrase 
					for keyphrase in listt2 ])
	keyphrases2=dict(keyphrases2)
	listresult2=[]
	for key in keyphrases2:
		listresult2.append({'key':key,'count':keyphrases2[key]})
	
	listresult2=sorted(listresult2, key=itemgetter('count'), reverse=True)
	return listresult2
	


	
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

def get_comment_list(api,post_id):
	comment_list_=[]
	hii=api.media_comments(post_id)
	for i in hii:
		comment_list_.append({"id": i.id,"text": i.text})
	return comment_list_



def get_list_of_media_comments_location(api,location_id,**option):
	
	all_comments_list_=[]
	tag_list_=[]

	if not location_id is None:
		epoch = datetime.datetime.utcfromtimestamp(0)
		if 'until' in option:
			untiltime=option['until']
		else:
			untiltime=time.time()
		if 'since' in option:
			sincetime=option['since']
		else:
			sincetime=untiltime-86400
		loc_media,_next=api.location_recent_media(location_id=location_id)    
		for a in loc_media:
			post_epochtime=(a.created_time-epoch).total_seconds()
			if(post_epochtime>float(sincetime) and post_epochtime<float(untiltime)):
				try:
				
					comments_list=get_comment_list(api,a.id)
					all_comments_list_.extend(comments_list)
				
				except:
					print 'no comments in media id %s :'% a.id
					continue
		try:
			exit=False
			while _next :
				more_loc_media,_next=api.location_recent_media(location_id=location_id,with_next_url=_next)
				for a in more_loc_media:
					post_epochtime=(a.created_time-epoch).total_seconds()
					if(post_epochtime>float(sincetime) and post_epochtime<float(untiltime)):
						try:
							comments_list=get_comment_list(api,a.id)
							all_comments_list_.extend(comments_list)
						

						except:
							print 'no comments in media id %s :'% a.id
							continue
					elif(post_epochtime<float(sincetime)):
						exit=True
						break
				if exit:
					break
		except:
			pass

	return all_comments_list_
