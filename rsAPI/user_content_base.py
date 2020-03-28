# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 21:14:54 2019

@author: OWNER
"""
import pandas as pd 

class user_content_base:
    
    def __init__(self, df):
        self.df  =df
    
    def get_recommendations(self,user_data,icb,n=10):
        user_data= user_data.merge(self.df,on='id')
        
        cast = user_data["cast"]
        cast =  cast.apply(pd.Series).reset_index().melt(id_vars='index').dropna()[['index', 'value']].set_index('index')
        cast = cast["value"].value_counts()[:5]
        
        genres = user_data["genres"]
        genres = genres.apply(pd.Series).reset_index().melt(id_vars='index').dropna()[['index', 'value']].set_index('index')
        genres = genres["value"].value_counts()[:5]
        
        keywords = user_data["keywords"]
        keywords = keywords.apply(pd.Series).reset_index().melt(id_vars='index').dropna()[['index', 'value']].set_index('index')
        keywords = keywords["value"].value_counts()[:5]
        
        director = user_data["director"]
        director = director.apply(pd.Series).reset_index().melt(id_vars='index').dropna()[['index', 'value']].set_index('index')
        director = director["value"].value_counts()[:5]
        user_data_soup = ' '.join(director.index) + ' ' + ' '.join(cast.index) + ' ' + ' '.join(genres.index) + ' ' + ' '.join(keywords.index)   
        user = pd.DataFrame([user_data_soup],columns={'soup'})
        return icb.get_similiraity_to_new_profile(user,n)
        