from .lib import Twitter_Analytics_Utils
from .._common_lib import common_functions
from collections import Counter
import datetime
import time
import json
import tweepy
import operator
from operator import itemgetter


class topics_from_network_with_sentiment:

    def execute(self,**params):
        """parse the parameters"""
        
        if ('twitter_consumer_key' in params) and ('twitter_consumer_secret' in params) and ('twitter_access_token' in params) and ('twitter_access_token_secret' in params):
            CONSUMER_KEY = params['twitter_consumer_key']
            CONSUMER_SECRET = params['twitter_consumer_secret']
            ACCESS_TOKEN = params['twitter_access_token']
            ACCESS_TOKEN_SECRET = params['twitter_access_token_secret']
        else:
            return 1, "Topic Page : Missing Twitter token information"

        if ('twitter_profile_id' in params):
            profile_id = int(params['twitter_profile_id'])
        else:
            return 2, "Topic Page : Missing Twitter Profile Identifier"

        if ('timespan' in params):
            timespan = int(params['timespan'])
        else:
            timespan = 1
            
        if ('until' in params):
            end_time = int(params['until'])
        else:
            time_now = int (time.time())
            end_time = time_now
            
        if ('since' in params): 
            if int(params['since']) < end_time:
                start_time = int(params['since'])
        else:
            start_time = end_time - 86400
            
        auth = tweepy.OAuthHandler (CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token (ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API (auth)

        return self.Trending_Topics_from_Netwrok_with_Sentiment_Analysis(start_time = start_time, end_time = end_time, profile_id = profile_id, timespan = timespan, api = api)

    # curl -X POST -H "Content-type: application/json" -d '{"analysis_type":"trending_topics_from_netwrok_with_sentiment_analysis","parameters":{"twitter_profile_id":"104856942", "since": "1484151355" , "until": "1484756155", "timespan": 5}}' http://127.0.0.1:5000/analyze/twitter

    def Trending_Topics_from_Netwrok_with_Sentiment_Analysis(self, start_time, end_time, profile_id, timespan, api):
        timespan_epoch = timespan * 86400
        pattern = '%Y-%m-%d %H:%M:%S'
        time_now = int (time.time())
        user_timeline = api.user_timeline(user_id = profile_id)
        listofkeyphrase = []
        retweeters = {}
        
        for status in user_timeline:
            created_epoch_time = int(time.mktime(time.strptime(str(status.created_at), pattern)))
            if time_now - created_epoch_time <= timespan_epoch:
                retweeter_ids = api.retweeters(id = status.id)
                for retweeter_id in retweeter_ids:
                    retweeters = Twitter_Analytics_Utils.add_retweeter(user_id = retweeter_id, retweeters = retweeters)
        
        retweeters_sorted = sorted(retweeters.items(), key=operator.itemgetter(1), reverse=True)
        best_retweeters = retweeters_sorted[5:10]
        print 'best reweeters : '
        print best_retweeters
        
        list_text_for_sentiment = []
        list_text_for_sentiment = Twitter_Analytics_Utils.get_retweeters_statuses(api = api, retweeter_ids = best_retweeters, start_time = start_time, end_time = end_time, list_text_for_sentiment = list_text_for_sentiment)

        print ("length of list text for sentiment = %d" %len(list_text_for_sentiment))
        length = len(list_text_for_sentiment)

        base_url = 'https://westus.api.cognitive.microsoft.com/'
        account_key = '5258e2016a2745dd9b3aa53f6dabc690'
        headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
        
        count = 0
        key_phrases = []
        while(count * 1000 < length):
            key_phrases.extend(common_functions.get_topic_in_positivecomments(list_text_for_sentiment[count * 1000:min((count + 1) * 1000, length)],base_url,headers))
            count = count + 1

        listresult = []
        keyphrases = Counter([keyphrase 
                    for keyphrase in key_phrases])
        keyphrases=dict(keyphrases)
        for key in keyphrases:
            listresult.append({'key':key,'count':keyphrases[key]})
        
        if len(listresult) == 0:
            redacted = True
            return redacted, "Trending Topics Container is Empty"
        redacted = False
        listresult=sorted(listresult, key=itemgetter('count'), reverse=True)

        return redacted, listresult
