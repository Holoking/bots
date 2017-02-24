import googlemaps
import tweepy
from config import Twitter_Tokens
import config

import json
import unicodedata
import urllib2
from collections import Counter


def initiate_tweepy_api():
    Twitter_Tokens.last_token_index = (Twitter_Tokens.last_token_index + 1) %4
    token_credentials = Twitter_Tokens.tokens_credentials[Twitter_Tokens.last_token_index]

    CONSUMER_KEY = token_credentials['CONSUMER_KEY']
    CONSUMER_SECRET = token_credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = token_credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = token_credentials['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler (CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token (ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    return api


def initiate_google_maps_api(google_account_key):
    
    google_maps = googlemaps.Client(google_account_key)

    return google_maps


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
        input_text = createAnalysAPIinputtext(list_by_limit, base_url, headers)
        obj = keyphrasesanalys(base_url,input_text,headers)
        count = count + 1

        for ob in obj['documents']:
            listofkeyphrase.extend(ob['keyPhrases'])
            
    keyphrases = Counter([keyphrase 
                    for keyphrase in listofkeyphrase])
    keyphrases=dict(keyphrases)
    for key in keyphrases:
        listresult.append({'key':key,'count':keyphrases[key]})        

    return listresult


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


def keyphrasesanalys(base_url,input_texts,headers):
    
    batch_sentiment_url = base_url +'text/analytics/v2.0/keyPhrases'
    
    req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    
    return obj


def languageanalys(base_url,input_texts,headers):
    
    num_detect_langs=1
    language_detection_url = base_url + 'text/analytics/v2.0/languages' + ('?numberOfLanguagesToDetect=' + num_detect_langs if num_detect_langs > 1 else '')
    
    req = urllib2.Request(language_detection_url, input_texts, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)

    return obj


def cleaning_text(text_):
    
    textout=text_.encode('ascii', 'replace').replace('\r',' ').replace('\\','').replace('"',' ').replace('\n',' ').replace("'"," ").replace('?','').replace('https//','')

    return textout


def add_hashtag(hashtag, hashtags = {}):
    
    if hashtag in hashtags:
        hashtags[hashtag] = hashtags[hashtag] + 1
    else:
        hashtags[hashtag] = 1
    
    return hashtags
