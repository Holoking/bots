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


def getnposts(FBgrah,Pageid,fields='{id,message}',**option):
	existnext =0
	post_list=[]
	t='posts loaded'
	nombre1=1000

	# Fill the FBgraph needed **kwargs 
	fb_options = {}

	Fields='posts'

	if 'since' in option:
		Fields+='.since('+str(option['since'])+')'
	else:
		sinceyesterday=time.time()-86400
		Fields+='.since('+str(int(sinceyesterday))+')'

	if 'nombre' in option:
		nombre1=int(option['nombre'])
		Fields+='.limit('+str(option['nombre'])+')'

	if 'until' in option:
		Fields+='.until('+str(option['until'])+')'

	Fields+=str(fields)

	fb_options['fields'] = Fields

	if 'date_format' in option:
		fb_options['date_format'] = option['date_format']

	#try:
	k=0
	posts = FBgrah.get_object(id=Pageid,**fb_options)['posts']

	for post in posts['data']:

		if 'message' in post:
			post['text'] = post['message']

		post.pop('message',None)
		post_list.append(post)
		
		if len(post_list)==nombre1:
			break
	try:
						 
		r=posts['paging']['next']
		i=0
		h=len(post_list)
		while h+k < nombre1  :   #max(len(input)) for microsoftapi = 1000
			try:
				# Attempt to make a request to the next page of data, if it exists.
				posts2=requests.get(r).json()
				posts2=dict(posts2)
				for post2 in posts2['data']:
					try:
						if 'message' in post2:
							post2['text'] = post2['message']
						post2.pop('message',None)
						post_list.append(post2)

						if len(post_list)==nombre1:
							break
					except KeyError:
						i+=1
						continue 
				h=len(post_list)+i        
				r=posts2['paging']['next']

			except KeyError:
				t='nonext listofallposts loaded'
				return post_list ,existnext ,t
		   
		existnext=1
		return post_list ,existnext ,r
	except KeyError:
		t='nonext listofallposts loaded'
		return post_list ,existnext ,t



def get1000comments(FBgrah,Postid,Fields='{id,message}'):
	existnext =0
	comment_list=[]
	Field='comments.limit(25)'+Fields
	k=0
	try:
		comments = FBgrah.get_object(id=Postid,fields=Field)['comments']
		
		for comment in comments['data']:
			try:
				comment_list.insert(len(comment_list),{'id':comment['id'] , 'text' : comment['message']}) 
			except KeyError:
				k+=1
				continue
		try:
			i=0
			r=comments['paging']['next']
			h=len(comment_list)
			while h+k<1000:   #max(len(input)) for microsoftapi = 1000
				try:
					# Attempt to make a request to the next page of data, if it exists.
					comments2=requests.get(r).json()
					comments2=dict(comments2)                                             
					for comment2 in comments2['data']:
						try:
							
							comment_list.insert(len(comment_list),{'id':comment2['id'] , 'text' : comment2['message']})
							if len(comment_list)+i+k==1000:
								break
						except KeyError:
							i+=1
							continue
					h=len(comment_list)+i
					r=comments2['paging']['next']


				except KeyError:
					t='nonext'
					return comment_list ,existnext ,t
					# When there are no more pages (['paging']['next']), break from the
						#loop and end the script.
					break
					
			existnext=1
			return comment_list ,existnext ,r  
		except KeyError:
			t='nonext'
			return comment_list ,existnext ,t 

	except (facebook.GraphAPIError,KeyError) as er:
		if type(er) ==facebook.GraphAPIError:
			t='can\'t access to posts\' comments or token problem'
			return comment_list ,existnext ,t
		else:
			t='can\'t access to posts\' comments or token problem'
			return comment_list ,existnext ,t



def getnext(url):
	listnextcomments=[]
	k=0
	while len(listnextcomments)+k<1000:        
		try:
			# Attempt to make a request to the next page of data, if it exists.
			posts2=requests.get(url).json()
			posts2=dict(posts2)
			for post2 in posts2['data']:
				try:
					listnextcomments.insert(len(listnextcomments),{'id':post2['id'] , 'text' : post2['message']})
					if len(listnextcomments)+k==1000:
						break
				except KeyError:
					k+=1
					
					continue
			url=posts2['paging']['next']
		except KeyError:
			t='nonext listofallposts loaded'
			existnext=0
			return listnextcomments ,existnext ,t  
			# When there are no more pages (['paging']['next']), break from the
			#loop and end the script.
			break
	existnext=1
	return listnextcomments ,existnext ,url
