# -*- coding: utf-8 -*-
"""
@author: YASH SAINI
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import cross_val_score,cross_val_predict
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
import csv

college_name=raw_input("Enter the name of the college:")
k = "FINAL_" + college_name + "_SENTIMENTS.csv"
df=pd.read_csv(k)
df.dropna(inplace=True)
tweet=[ i for i in df['Tweets']]
d1={'Happiness':1,'Neutral':0,'Anger':-2,'Fear':-3,'Disgust':-4,'Sadness':-1}
df['Sentiment']=df['Sentiment'].map(d1)

''' Used for forming feature vectors through bag of words technique'''
'''
#y=[]
for i in range(len(df)):
    l.append([df.loc[i,'Happiness'],df.loc[i,'Anger'],df.loc[i,'Fear'],df.loc[i,'Sadness'],df.loc[i,'Disgust']]) 
    #y.append(df.loc[i,'Sentiment'])
'''
cv = CountVectorizer(token_pattern='(?u)\\b\\w+\\b',max_features = 2000)
X = cv.fit_transform(tweet).toarray()
y=df.loc[:,'Sentiment'].values
X_train,X_test,Y_train,Y_test= train_test_split(X,y,train_size=0.7,random_state=42)

scoring_r=[]
scoring_t=[]
'''
with open("SCORES_Test" +".csv", 'w+') as csv_file:
   writer = csv.writer(csv_file)
   writer.writerow(("College","KNN", "SVM", "Naive_Bayes"))

with open("SCORES_Training"+".csv", 'w+') as csv_file:
   writer = csv.writer(csv_file)
   writer.writerow(("College","KNN", "SVM", "Naive_Bayes"))
'''
     
def print_score(clf,X_train,Y_train,X_test, Y_test,train=True):
    if train:
        print("\nTraining Result:")
        print("\naccuracy_score: \t {0:.4f}".format(accuracy_score(Y_train,clf.predict(X_train))))
        print("\nClassification_report: \n{}\n".format(classification_report(Y_train,clf.predict(X_train))))
        print("Confusion Matrix: \n {}\n".format(confusion_matrix(Y_train,clf.predict(X_train))))
        
        res=cross_val_score(clf,X_train,Y_train,cv=10,scoring="accuracy")
        print("Average Accuracy:\t {0:.4f}".format(np.mean(res)))
        print ("Accuracy SD:\t\t {0:.4f}".format(np.std(res)))
        return "{0:.4f}".format(accuracy_score(Y_train,clf.predict(X_train)))
    
    elif train==False:
        print("\nTest Results:")
        print("\naccuracy_score: \t {0:.4f}".format(accuracy_score(Y_test,clf.predict(X_test))))
        print("\nClassification_report: \n{}\n".format(classification_report(Y_test,clf.predict(X_test))))
        print("\nConfusion Matrix:\n{}\n".format(confusion_matrix(Y_test,clf.predict(X_test))))
        return "{0:.4f}".format(accuracy_score(Y_test,clf.predict(X_test)))

"""KNN"""
knn= KNeighborsClassifier(n_neighbors=5,p=2,metric='minkowski')
knn.fit(X_train,Y_train)
print ("\n \t\t------KNN Classifier----\n")       
#Scores for training data
v=print_score(knn,X_train,Y_train,X_test, Y_test,train=True)
#Scores for test data
t=print_score(knn,X_train,Y_train,X_test, Y_test,train=False)
scoring_r.append(v)
scoring_t.append(t)

'''SVM'''
clf=svm.SVC(kernel='rbf', degree=3,  gamma=0.7)
clf.fit(X_train,Y_train)

print("\n\n\t\t----- SVM Details-------\n\n")
#Scores for training data
v=print_score(clf,X_train,Y_train,X_test, Y_test,train=True)
#Scores for test data
t=print_score(clf,X_train,Y_train,X_test, Y_test,train=False)
scoring_r.append(v)
scoring_t.append(t)

""" Naive Bayes"""
model = GaussianNB()
model.fit(X_train,Y_train)
print("\n\n Naive Bayesian\n\n")
#Scores for training data
v=print_score(model,X_train,Y_train,X_test, Y_test,train=True)
#Scores for test data
t=print_score(model,X_train,Y_train,X_test, Y_test,train=False)
scoring_r.append(v)
scoring_t.append(t)

''' Append the accuracy to the scores file for further analysis''' 
with open("SCORES_Training" +".csv", 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow((college_name,scoring_r[0], scoring_r[1],scoring_r[2]))

with open("SCORES_Test" +".csv", 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow((college_name,scoring_t[0], scoring_t[1],scoring_t[2]))
    
# Read the datafile and plot 
""" For different colleges different ML techniques perform differently
dg=pd.read_csv("SCORES_Training" +".csv")
dg.plot(x="College", y=["KNN","SVM","Naive_Bayes"], kind="bar",figsize=(8,5))

dg=pd.read_csv("SCORES_Test" +".csv")
dg.plot(x="College", y=["KNN","SVM","Naive_Bayes"], kind="bar",figsize=(8,5))


"""