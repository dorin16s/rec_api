# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:40:00 2019

@author: OWNER
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class item_content_base:
    def __init__(self,df):
        self.df = df
        tfidf = TfidfVectorizer(stop_words='english')
        df['overview'] = df['overview'].fillna('')
        tfidf_matrix = tfidf.fit_transform(df['overview'])
        self.cosine_sim_overview = linear_kernel(tfidf_matrix, tfidf_matrix)
        self.indices = pd.Series(df.index, index=df['title']).drop_duplicates()
        
        self.count = CountVectorizer(stop_words='english')
        self.count_matrix = self.count.fit_transform(df['soup'])
        self.cosine_sim_features = cosine_similarity(self.count_matrix, self.count_matrix)

    
    def get_similiraity_to_new_profile(self,user_data_soup,n=10):
        user_count_matrix = self.count.transform(user_data_soup['soup'])
        cosine_sim_features = cosine_similarity(self.count_matrix, user_count_matrix)
        sim_scores = list(enumerate(cosine_sim_features))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        return self.df['title'].iloc[movie_indices]

    def get_recommendations(self,title, sim_method,n=10):
        idx = self.indices[title]
        
        if sim_method=="overview":
            cosine_sim = self.cosine_sim_overview   
        else:
            cosine_sim=self.cosine_sim_features
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        x= (self.df[['title','soup']].iloc[movie_indices])
        y= (self.df[['title','soup']].iloc[idx])

        return self.df['title'].iloc[movie_indices] , sim_scores,x,y