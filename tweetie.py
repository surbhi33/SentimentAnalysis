#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 15:06:38 2021

@author: surbhiprasad
"""

import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename,encoding='utf-8-sig') as f:
        items = f.readline().strip().split(',')
        return items

#keys=loadkeys("/Users/surbhiprasad/twitter.csv")


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    api_hit=loadkeys(twitter_auth_filename)
    ACCESS_TOKEN = api_hit[2]
    ACCESS_SECRET = api_hit[3]
    CONSUMER_KEY = api_hit[0]
    CONSUMER_SECRET = api_hit[1]
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    api = tweepy.API(auth,wait_on_rate_limit=True)
    
    return api


#new_trial=authenticate("/Users/surbhiprasad/twitter.csv")


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    user_name=api.get_user(screen_name=name)
    analyser = SentimentIntensityAnalyzer()
    
    tweets_ls=[]
    person_tweets = api.user_timeline(screen_name=name,count=100)
    
    for tweet in person_tweets:
        id_tweet=tweet.id
        created=tweet.created_at
        retweeted=tweet.retweet_count
        text=tweet.text
        hashtags=[x['text'] for  x in tweet.entities.get('hashtags')]
        urls=[x['url'] for  x in tweet.entities.get('urls')]
        mentions=[x['screen_name'] for  x in tweet.entities.get('user_mentions')]
        
        score=analyser.polarity_scores(text)['compound']
        tweets_ls.append({'id':id_tweet, 
                  'created':created, 
                  'retweeted':retweeted, 
                  'text':text, 
                  'hashtags':hashtags,
                  'urls':urls,
                  'mentions':mentions,
                  'score':score})
        
        
    dict_all_tweets={}
    dict_all_tweets['user']=user_name.screen_name
    dict_all_tweets['count']=len(tweets_ls)
    dict_all_tweets['tweets']=tweets_ls
    
    return dict_all_tweets



#all_tweets=fetch_tweets(api_hit, 'the_antlr_guy')

def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get the list of User objects back from friends();
    get a maximum of 100 results. Pull the appropriate values from
    the User objects and put them into a dictionary for each friend.
    """
    friends_ls=[]
    for friend in api.get_friends(screen_name=name,count=100):
        #friend_name=api.get_user(screen_name=friend)
        
        dict_user={}
        dict_user['name']=friend.name
        dict_user['screen_name']=friend.screen_name
        dict_user['followers']=friend.followers_count
        dict_user['created']=friend.created_at.strftime('%Y-%m-%d')
        dict_user['image']=friend.profile_image_url_https 
        
        friends_ls.append(dict_user)
        
    return friends_ls


#following=fetch_following(api_hit, 'the_antlr_guy')
    
    
