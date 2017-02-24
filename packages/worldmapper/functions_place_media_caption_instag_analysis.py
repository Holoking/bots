from instagram.client import InstagramAPI
import datetime
import time
from operator import itemgetter
from collections import Counter
import re
import instagram_common_function


def get_hashtags_medias_captions_location(tag_list_):
	keyphrases=Counter([a 
			for a in tag_list_])
	keyphrases=dict(keyphrases)
	listtag=[]
	for key in keyphrases:
		listtag.insert(len(listtag),{'key':'#'+key,'count':keyphrases[key]})
	listtag=sorted(listtag, key=itemgetter('count'), reverse=True)
	return listtag



def get_list_of_media_caption_tags_location(api,location_id,**option):
	
	caption_list_=[]
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
				
					caption_list_.append({"id": a.id,"text": a.caption.text})
					for c in a.tags:
						tag_list_.append(c.name)

				except:
					print 'no text in media id %s :'% a.id
					continue
		try:
			exit=False
			while _next :
				more_loc_media,_next=api.location_recent_media(location_id=location_id,with_next_url=_next)
				for a in more_loc_media:
					post_epochtime=(a.created_time-epoch).total_seconds()
					if(post_epochtime>float(sincetime) and post_epochtime<float(untiltime)):
						try:
							caption_list_.append({"id": a.id,"text": a.caption.text})
							for c in a.tags:
								tag_list_.append(c.name)                

						except:
							print 'no text in media id %s :'% a.id
							continue
					elif(post_epochtime<float(sincetime)):
						exit=True
						break
				if exit:
					break
					
				
		except:
			pass

	return caption_list_,tag_list_
