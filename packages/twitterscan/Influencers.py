
# coding: utf-8

# In[20]:

import tweepy
import time
import operator
import Influencer_Utils


def get_followers_number(user_id, api):
    user = Influencer_Utils.get_user(user_id, api)
    followers_number = user.followers_count
    
    result = []
    result.append({"Followers Number":followers_number})
    
    return result


def get_friends_number(user_id, api):
    user = Influencer_Utils.get_user(user_id, api)
    friends_number = user.friends_count
    
    result = []
    result.append({"Friends Number":friends_number})
    
    return result


def get_keywords_by_topic(topic, api):
    key_words = {}
    for status in tweepy.Cursor(api.search, q = topic, ).items():
        status_hashtags = status.entities['hashtags']
        for hashtag in status_hashtags:
            key_words = Influencer_Utils.add_hashtag(hashtag['text'], key_words)
    
    return key_words


def get_influencers_from_keyword(keyword, api):
    profiles_result = []
    query = str(keyword)
    
    try:
        for item in tweepy.Cursor(api.search_users, q = query).items():
            profiles_result.append({"id":int(item.id_str), "name":item.name, "followers":int(item.followers_count)})
    except Exception as exc:
        print exc
    
    return profiles_result 


def get_influencers_from_hashtag(hashtag, api):
    profiles_result = []
    query = "#" + str(hashtag)
    
    try:
        for item in tweepy.Cursor(api.search_users, q = query).items():
            profiles_result.append({"id":int(item.id_str), "name":item.name, "followers":int(item.followers_count)})
    except Exception as exc:
        print exc
    
    return profiles_result


def get_influencers_from_bio(topic, api):
    profiles_result = []
    query = "i tweet about " + str(topic)
    
    try:
        for item in tweepy.Cursor(api.search_users, q = query).items():
            profiles_result.append({"id":int(item.id_str), "name":item.name, "followers":int(item.followers_count)})
    except Exception as exc:
        print exc
    
    return profiles_result


def average_likes_number_per_post(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    likes_average = float(0)
    data_length = len(likes_data)
    for post_time, likes_count in likes_data:
        likes_average = float(likes_average) + (float(likes_count) / data_length)
    
    result = []
    result.append({"Average Likes Number per Post":likes_average})
    
    return result


def average_retweets_number_per_post(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    retweets_average = float(0)
    data_length = len(retweets_data)
    for post_time, retweets_count in retweets_data:
        retweets_average = float(retweets_average) + (float(retweets_count) / data_length)
    
    result = []
    result.append({"Average Retweets Number per Post":retweets_average})
    
    return result


def average_likes_number_per_day(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    likes_by_day = Influencer_Utils.calculate_average_by_day(timestamp = 3600 * 24, data = likes_data)
    
    likes_average_per_day = float(0)
    data_length = len(likes_by_day)
    for like in likes_by_day:
        likes_average_per_day = likes_average_per_day + likes_by_day[like]
        
    likes_average_per_day = (float(likes_average_per_day)) / data_length
    
    result = []
    result.append({"Average Likes Number per Day":likes_average_per_day})
    result.append({"Average Likes Number By Day":likes_by_day})
    
    return result
    

def average_retweets_number_per_day(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    retweets_by_day = Influencer_Utils.calculate_average_by_day(timestamp = 3600 * 24, data = retweets_data)
    
    retweets_average_per_day = float(0)
    data_length = len(retweets_by_day)
    for retweet in retweets_by_day:
        retweets_average_per_day = retweets_average_per_day + retweets_by_day[retweet]
        
    retweets_average_per_day = (float(retweets_average_per_day)) / data_length
    
    result = []
    result.append({"Average Retweets Number per Day":retweets_average_per_day})
    result.append({"Average Retweets Number By Day":retweets_by_day})
    
    return result


def likes_growth_rate_day_per_day(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    likes_by_day = Influencer_Utils.calculate_average_by_day(timestamp = 3600 * 24, data = likes_data)
    
    counter = 1
    likes_growth_rate = {}
    while(counter < len(likes_by_day)):
        key = str(counter + 1) + "/" + str(counter)
        value = float(likes_by_day[str(counter + 1)]) / likes_by_day[str(counter)]
        likes_growth_rate[key] = value
        counter = counter + 1
    
    likes_growth_sorted = sorted(likes_growth_rate.items(), key = operator.itemgetter(0))
    
    result = []
    result.append({"Likes Growth Rate Day by Day":likes_growth_sorted})
    
    return result


def retweets_growth_rate_day_per_day(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    retweets_by_day = Influencer_Utils.calculate_average_by_day(timestamp = 3600 * 24, data = retweets_data)
    
    counter = 1
    retweets_growth_rate = {}
    while(counter < len(retweets_by_day)):
        key = str(counter + 1) + "/" + str(counter)
        value = float(retweets_by_day[str(counter + 1)]) / retweets_by_day[str(counter)]
        retweets_growth_rate[key] = value
        counter = counter + 1
    
    retweets_growth_sorted = sorted(retweets_growth_rate.items(), key = operator.itemgetter(0))
    
    result = []
    result.append({"Retweets Growth Rate Day by Day":retweets_growth_sorted})
    
    return result


def total_Engagement_by_Reach(user_id, api):
    
    likes_data, retweets_data = Influencer_Utils.get_metrics_history(user_id = user_id, api = api, period = 3600 * 24 * 7)
    
    total_engagement = 0
    for a,b in likes_data:
        total_engagement = total_engagement + b
    
    for a,b in retweets_data:
        total_engagement = total_engagement + b
    
    user = Influencer_Utils.get_user(user_id, api)
    
    followers_count = get_followers_number(user_id, api)[0]['Followers Number']
    try:
        engagement_by_reach = float(total_engagement) / followers_count
    except:
        engagement_by_reach = 0
    
    result = []
    result.append({"Total Engagement by Total Reach Rate":engagement_by_reach})
    
    return result
