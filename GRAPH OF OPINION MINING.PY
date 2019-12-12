# -*- coding: utf-8 -*-
"""

@author: YASH
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def graph(c):
    
    har=[0,0,0,0,0,0]
    for i in c:
        if i=='Happiness':
            har[0]+=1
        elif i=='Anger':
            har[1]+=1
        elif i=='Neutral':
            har[5]+=1
        elif i=='Fear':
            har[2]+=1
        elif i=='Sadness':
            har[3]+=1
        elif i=='Disgust':
            har[4]+=1
    s=float(sum(har))
    for i in range(len(har)):
        har[i]=har[i]/s
    return har


harvard=pd.read_csv("FINAL_Harvard_SENTIMENTS.csv")
mit=pd.read_csv("FINAL_MIT_SENTIMENTS.csv")
stanford=pd.read_csv("FINAL_Stanford_SENTIMENTS.csv")

har=graph(harvard['Sentiment'].values)
mit=graph(mit['Sentiment'].values)
stan=graph(stanford['Sentiment'].values)

Index=['Happiness','Anger','Fear','Sadness','Disgust','Neutral']
gr={'Harvard':har,'MIT':mit,'Stanford':stan}
qw=pd.DataFrame(gr,index=Index)
qw.plot(y=["Harvard","MIT", "Stanford"],kind="bar")
y.label='Number of tweets'
plt.show()

        
    
    
    
        
    
                
                    
                
                
                

    
        
        
    
            
    