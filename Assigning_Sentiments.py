# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 12:22:06 2019

@author: YASH
"""
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize 
from nltk.stem.porter import PorterStemmer
import csv
import pandas as pd
import numpy 

#Data cleaning Functions:
def isEnglish(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

    #The following function removes the part of the string that contains the substring eg. if
    #substring = 'http' , then http://www.google.com is removed, that means, remove until a space is found
def rem_substring(tweets,substring):
    m=0;
    for i in tweets:
        if (substring in i):
        #while i.find(substring)!=-1:
            k=i.find(substring)
            d=i.find(' ',k,len(i))
            if d!=-1:               #substring is present somwhere in the middle(not the end of the string)
                i=i[:k]+i[d:]
            else:                   #special case when the substring is present at the end, we needn't append the
                i=i[:k]             #substring after the junk string to our result
        tweets[m]=i #store the result in tweets "list"
        m+= 1
    return tweets
def removeNonEnglish(tweets):
    result=[]
    for i in tweets:
        if isEnglish(i):
            result.append(i)
    return result

#the following function converts all the text to the lower case
def lower_case(tweets):
    result=[]
    for i in tweets:
        result.append(i.lower())
    return result

def rem_punctuation(tweets):
    #print(len(tweets))
    m=0
    validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for i in tweets:
        x = ""
        for j in i:
            if (j in validLetters)==True:
                x += j
        tweets[m]=x
        m=m+1
    return tweets

def stop_words(tweets):
    #Removal of Stop words like is, am , be, are, was etc.
    stop_words1 = set(stopwords.words('english')) 
    indi=0
    for tweet in tweets:
        new_s=[]
        Br_tweet = word_tokenize(tweet)
        for word in Br_tweet:
            if (word not in stop_words1):
                new_s.append(word)
        et=" ".join(new_s)
        tweets[indi]=et
        indi+=1
    return tweets
        
                

def score(college_name):
    filename = 'data_emotions_words_list.csv'
    pos_file_name= "Pos_tagged_" + college_name + ".csv"
    POS=pd.read_csv(pos_file_name)
    POS_tweets=POS['POS_Tweet'].values
    adverb1=pd.read_csv("adverb.csv")
    verb1=pd.read_csv("verb.csv")
    
    ''' Verb and adverb are dictionaries having values for verbs and adverbs'''
    verb={};adverb={}
    l=adverb1['value'].values
    j=0
    for i in adverb1['adverb'].values:
        adverb[i]=l[j]
        j+=1
    l=verb1['Value'].values
    j=0
    for i in verb1['Verb'].values:
        verb[i]=l[j]
        j+=1
    
    ''' Add the adjectives in the dictionary'''
    
    Adjectives={}
    df=pd.read_csv("data_emotions_words_list.csv")
    for i in range(len(df)) : 
        Adjectives[df.loc[i, "Words"]]= [df.loc[i, "Happiness"],df.loc[i, "Anger"],df.loc[i, "Sadness"],df.loc[i, "Fear"],df.loc[i, "Disgust"]] 

    ''' Assign Scores to each tweet'''
    FINAL={};FINAL1={'Tweets':[],'Happiness':[],'Sadness':[],'Fear':[],'Disgust':[],'Anger':[],'Sentiment':[]}
    for tweet in POS_tweets:
        sum_adverb=0;sum_verb=0
        score_list=[]
        words=word_tokenize(tweet)
        stem=stemming(words)
        f_stem=0
        for i in words :
            if (i in adverb):
                sum_adverb+=adverb[i]
    
                
            elif (stem[f_stem] in adverb):
                sum_adverb+=adverb[stem[f_stem]]
               
                
            elif (i in verb):
                sum_verb+=verb[i]
                
                
            elif (stem[f_stem] in verb):
                sum_verb+=verb[stem[f_stem]]
            else:
                if (i in Adjectives ) or (stem[f_stem] in Adjectives):
                    if i in Adjectives:
                        # ADJ=[Happiness,Anger,Sadness,Fear,disgust]
                        ADJ=Adjectives[i]
                    elif (stem[f_stem] in Adjectives):
                        ADJ=Adjectives[stem[f_stem]]
                    else:
                        pass
                    
                    # Calculate Score
                    c=sum_adverb + sum_verb
                    #The formula is derived from the research paper
                    if (c) <0 :
                        for j in range(len(ADJ)):
                            ADJ[j]=5.0-ADJ[j]
                    elif (c>=0.5):
                        for j in range(len(ADJ)):
                            ADJ[j]=c*ADJ[j]
                    else:
                        for j in range(len(ADJ)):
                            ADJ[j]=0.5*ADJ[j]
                    score_list.append(ADJ)
                    sum_adverb=0;sum_verb=0
            f_stem+=1
        total_adj=len(score_list)
        s=[0.0 for i in range(5)]
        emo=''
        if (total_adj != 0):
            for i in score_list:
                s[0]+=i[0] #Happiness
                s[1]+=i[1]#Anger
                s[2]+=i[2] #Sadness
                s[3]+=i[3] #Fear
                s[4]+=i[4] #Disgust
            for i in range(len(s)):
                s[i]= "{0:.6f}".format(s[i]/total_adj)
            emotion=0.0
            for i in range(len(s)):
                if (s[i]> emotion):
                    emotion=max(emotion,s[i])
                    if i==0 :
                        emo='Happiness'
                    elif i==1:
                        emo='Anger'
                    elif i==2:
                        emo='Sadness'
                    elif i==3:
                        emo='Fear'
                    elif i==4:
                        emo='Disgust'
                
        else:
            # if adj is not in vocabulary assign 
            s=[0.2000 for i in range(5)]
            emo='Neutral'
            
        #find the Max emotion value for the tweet
        s.append(emo)
            
        
        #Add the final tweet and score
        FINAL[tweet]=s
        FINAL1['Tweets'].append(tweet)
        FINAL1['Happiness'].append(s[0])
        FINAL1['Anger'].append(s[1])
        FINAL1['Fear'].append(s[3])
        FINAL1['Sadness'].append(s[2])
        FINAL1['Disgust'].append(s[4])
        FINAL1['Sentiment'].append(s[5])
    DB=pd.DataFrame(FINAL1,columns=['Tweets','Happiness','Anger','Fear','Sadness','Disgust','Sentiment'])
    file_name = "FINAL_" + college_name + "_SENTIMENTS.csv"
    DB.to_csv(file_name)
        

 #POS Tagger Function used to identify the adjectives, verbs, adverbs.

def POS_tagger(tweets, username):
    final = []
        # for each line in tweets list
    for line in tweets:
        t = []
            # for each sentence in the line
            # tokenize this sentence
        text= word_tokenize(line)
        k = nltk.pos_tag(text)
        for i in k:
                # Only Verbs, Adverbs & Adjectives are Considered
                if ((i[1][:2] == "VB") or (i[1][:2] == "JJ") or (i[1][:2] == "RB")):
                    t.append(i[0])
        one_tweet=" ".join(t)
        if (len(one_tweet)>0):
            final.append(one_tweet)
    
    dict1={'POS_Tweet':final}
    db1=pd.DataFrame(dict1)
    filename = "Pos_tagged_" + username + ".csv"
    
    db1.to_csv(filename)

def stemming(tweets):
    # Find the root word
    # stemming of words
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in tweets]
    return stemmed

def main():
    c=raw_input("Enter the name of the raw_tweets college:")
    c_f=c+'_tweets.csv'
    db=pd.read_csv(c_f)
    tweets=list(db['text'])
    tweets=rem_substring(tweets,'#')
    tweets=rem_substring(tweets,'http')
    tweets=rem_substring(tweets,'https')
    tweets=rem_substring(tweets,'www')
    tweets=rem_substring(tweets,'@')
    tweets=rem_substring(tweets,'RT')
    
    tweets=rem_punctuation(tweets)
    tweets=stop_words(tweets)
    tweets= removeNonEnglish(tweets)
   
    tweets=lower_case(tweets)
    
    #tweets = stemming(tweets)
   
    
    #tweets.replace("."," ")
    for tweet in tweets:
        tweet=tweet.replace("."," ")

    
    dict1={'Tweet':tweets}
    db1=pd.DataFrame(dict1)
    r_f='cleaned_'+ c + '.csv'
    db1.to_csv(r_f)
    
     
    POS_tagger(tweets,c)
    print("Tweets have now been cleaned !!")
    score(c)

main()