import facebook
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


def getnposts(FBgrah,Pageid,fields='{id,message}',**option):
    existnext =0
    post_list=[]
    t='posts loaded'
    sincetime=time.time()-86400
    nombre1=1000

    Fields='posts'
    if 'since' in option:
        Fields+='.since('+str(option['since'])+')'
        sincetime=int(option['since'])
    if 'nombre' in option:
        nombre1=int(option['nombre'])
        Fields+='.limit('+str(option['nombre'])+')'
    if 'until' in option:
        Fields+='.until('+str(option['until'])+')'
    if len(option)==0:
        sinceyesterday=time.time()-86400
        Fields+='.since('+str(int(sinceyesterday))+')'

    Fields+=str("{id,message}")

    try:
        k=0
        posts = FBgrah.get_object(id=Pageid,fields=Fields)['posts']
        for post in posts['data']:
            try:
                post_list.insert(len(post_list),{'id':post['id'] ,'text':post['message']})

            except KeyError:
                k+=1
                continue 
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
                            post_list.insert(len(post_list),{'id':post2['id'] , 'text' : post2['message']})
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
                    # When there are no more pages (['paging']['next']), break from the
                     #loop and end the script.
                    break

            existnext=1
            return post_list ,existnext ,r
        except KeyError:
            t='nonext listofallposts loaded'
            return post_list ,existnext ,t   
    except (facebook.GraphAPIError,KeyError) as er:

        if type(er) ==facebook.GraphAPIError:
            t='can,t access to page posts or token problem'
            return post_list ,existnext ,t
        else:
            t='no posts since '+ str(sincetime)
            return post_list ,existnext ,t


def metrics_per_post(FBgrah,post_id):
    result=[]
    try :
        metric=FBgrah.get_object(id=post_id,fields='shares,comments.limit(0).summary(True),reactions.type(LIKE).limit(0).summary(true).as(like),reactions.type(LOVE).limit(0).summary(true).as(love),reactions.type(WOW).limit(0).summary(true).as(wow),reactions.type(HAHA).limit(0).summary(true).as(haha),reactions.type(SAD).limit(0).summary(true).as(sad),reactions.type(ANGRY).limit(0).summary(true).as(angry), reactions.type(THANKFUL).limit(0).summary(true).as(thankful)')
    except Exception as exc:
        print  str(exc)
        return result

    result=[{"key":"like","count":metric['like']['summary']['total_count']},{"key":"love","count":metric['love']['summary']['total_count']},{"key":"wow","count":metric['wow']['summary']['total_count']},{"key":"haha","count":metric['haha']['summary']['total_count'] },{"key":"sad","count":metric['sad']['summary']['total_count'] },{"key":"angry","count":metric['angry']['summary']['total_count'] },{"key":"thankful","count":metric['thankful']['summary']['total_count'] },{"key":"shares","count":metric['shares']['count']},{"key":"comment","count":metric['comments']['summary']['total_count']}]

    return result

def fan_count(FBgrah,page_id):
    print(FBgrah)
    print(page_id)
    count=FBgrah.get_object(id=page_id,fields='fan_count')['fan_count']
    print(str(count))
    return count

def get_user_metrics_for_the_days_of_this_week(FBgrah,page_id):
    since_=(datetime(datetime.now().year,datetime.now().month,datetime.now().day) - datetime(1970,1,1,0,0)).total_seconds()
    list_metrics=[]
    until_=since_+86400
    i=0
    while i<7:
        likes_counts=0
        comments_counts=0
        shares_counts=0
        list_posts_day=[]
        list_posts,existnext,next_url=getnposts(FBgrah,page_id,since=since_,until=until_)
        list_posts_day.extend(list_posts)
        while existnext==1:
            list_posts,existnext,next_url=getnposts(FBgrah,page_id,since=since_,until=until_)
            list_posts_day.extend(list_posts)
        

        for b in list_posts_day:
            h=metrics_per_post(FBgrah,b['id'])
            for a in h :
                if a['key'] in ['like','love','wow','haha','sad','angry','thankfull']:
                    likes_counts+=a['count']
                if a['key'] == 'comment':
                    comments_counts+=a['count']
                if a['key'] == 'shares':
                    shares_counts+=a['count']

        list_metrics.append({'date':str(datetime.fromtimestamp(since_)),'posts':len(list_posts_day),'comments':comments_counts,'likes':likes_counts,'shares':shares_counts})
        i+=1
        since_=since_-86400
        until_=since_+86400
    return list_metrics

def get_likes_comments_shares_posts_week_number(FBgrah,page_id):
    likes_week_number=0
    posts_week_number=0
    comments_week_number=0
    shares_week_number=0
    list_week_metrics=get_user_metrics_for_the_days_of_this_week(FBgrah,page_id)
    for metric_day in list_week_metrics:
        likes_week_number+=metric_day['likes']
        posts_week_number+=metric_day['posts']
        comments_week_number+=metric_day['comments']
        shares_week_number+=metric_day['shares']
    output=[{'date':str(datetime.now()),'likes_over_last_week':likes_week_number,'comments_over_last_week':comments_week_number,'posts_over_last_week':posts_week_number,'shares_over_last_week':shares_week_number}]
    return output

def get_list_of_average_by_day(FBgrah,page_id):
    output=[]
    list_week_metrics=get_user_metrics_for_the_days_of_this_week(FBgrah,page_id)
    for metric_day in list_week_metrics:
        if metric_day['posts']!=0:
            likes_day_average=float(metric_day['likes'])/metric_day['posts']
            comments_day_average=float(metric_day['comments'])/metric_day['posts']
            shares_day_average=float(metric_day['shares'])/metric_day['posts']
        else:
            likes_day_average=0
            comments_day_average=0
            shares_day_average=0
        output.append({'date':metric_day['date'],'likes_day_average':likes_day_average,'comments_day_average':comments_day_average,'shares_day_average':shares_day_average})
    return output

def Average_likes_number_per_post_over_last_week(FBgrah,page_id):
    list_week_metrics=get_likes_comments_shares_posts_week_number(FBgrah,page_id)
    if list_week_metrics[0]['posts_over_last_week']!=0:
        return [{'Average likes number per post over last week':(float(list_week_metrics[0]['likes_over_last_week'])/list_week_metrics[0]['posts_over_last_week'])}]
    else:
        return [{'Average likes number per post over last week':0}]

def Average_comments_number_per_post_over_last_week(FBgrah,page_id):
    list_week_metrics=get_likes_comments_shares_posts_week_number(FBgrah,page_id)
    if list_week_metrics[0]['posts_over_last_week']!=0:
        return [{'Average comments number per post over last week':(float(list_week_metrics[0]['comments_over_last_week'])/list_week_metrics[0]['posts_over_last_week'])}]
    else:
        return [{'Average comments number per post over last week':0}]
def Average_shares_number_per_post_over_last_week(FBgrah,page_id):
    list_week_metrics=get_likes_comments_shares_posts_week_number(FBgrah,page_id)
    if list_week_metrics[0]['posts_over_last_week']!=0:
        return [{'Average shares number per post over last week':(float(list_week_metrics[0]['shares_over_last_week'])/list_week_metrics[0]['posts_over_last_week'])}]
    else:
        return [{'Average shares number per post over last week':0}]

def Average_likes_number_per_day_over_last_week(FBgrah,page_id):
    list_day_average=get_list_of_average_by_day(FBgrah,page_id)
    week_per_day_average=0
    for day in list_day_average:
        week_per_day_average+=day['likes_day_average']

    return [{'Average likes number per day over last week':(float(week_per_day_average)/7)}]

def Average_comments_number_per_day_over_last_week(FBgrah,page_id):
    list_day_average=get_list_of_average_by_day(FBgrah,page_id)
    week_per_day_average=0
    for day in list_day_average:
        week_per_day_average+=day['comments_day_average']

    return [{'Average comments number per day over last week':(float(week_per_day_average)/7)}]
def Average_shares_number_per_day_over_last_week(FBgrah,page_id):
    list_day_average=get_list_of_average_by_day(FBgrah,page_id)
    week_per_day_average=0
    for day in list_day_average:
        week_per_day_average+=day['shares_day_average']

    return [{'Average shares number per day over last week':(float(week_per_day_average)/7)}]

def engagement_by_reach(FBgrah,page_id):
    list_week_metrics=get_likes_comments_shares_posts_week_number(FBgrah,page_id)
    engagement=list_week_metrics[0]['likes_over_last_week']+list_week_metrics[0]['comments_over_last_week']+list_week_metrics[0]['shares_over_last_week']
    follower=fan_count(FBgrah,page_id)
    return [{'engagement_by_reach':(float(engagement)/follower)}]
