# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:03:43 2019

@author: YASH
"""

import tweepy #https://github.com/tweepy/tweepy
import csv
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

#Twitter API credentials


consumer_key = 'pJACERyDqWQcafRZzxQj4gVX8'
consumer_secret = 'W4ye5LpkA9MvAB8HyNFDbkcGGVPMfSe8ArmPB3glm9kMITA7vx'
access_key = '2425709504-aWGkzlCkLHXZmu4uH1p5RZgjh2aTwCE835Zy2An'
access_secret = 'b4KJzIR0Vt3qhIBsm0jf26wqoUKCd3t9V8h271KZ2F9iM'


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []  

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass



#pass in the username of the account you want to download
get_all_tweets("Stanford")
