import facebook
import requests






def search_users_facebook(list_of_users):  #list_of_users from instagram or twitter
	list_of_infl_fb=[]
	for user_ in list_of_users:
		try:
			graph = facebook.GraphAPI(access_token='EAAW4yOBGazsBANv62ViY7dwKMgxbM2NW4YPscZBtX1YXCJSqpNFFREJ8ZBfRircO91k49X9I4YAebyZCMfERC9qIFv3chVQi2O2OJCA1u5P1y8ZCXmjGt4WyRR9wJtYv90q3kTL57bFBoZB6AWAim',version=2.7)
			L=graph.request('search', {'q': user_['name'], 'type': 'page'})
			page_talking=0
			offic_id=''
			name_fb=''
			for i in L['data']:
				g=graph.get_object(id=i['id'],fields='name,fan_count,talking_about_count')
				if g['talking_about_count']>page_talking :
					name_fb=g['name']
					offic_id=i['id']
					page_talking=g['talking_about_count']
					
			list_of_infl_fb.append({'name':name_fb,'id':offic_id})
		except Exception as er:
			print str(er)
			continue
			
	return list_of_infl_fb