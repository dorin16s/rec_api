import pandas as pd
from ast import literal_eval
import numpy as np
from rsAPI.item_content_base import item_content_base
from rsAPI.user_content_base import user_content_base


def prepare_data(df1, df2, df3):
    df1.columns = ['cast', 'crew', 'id']
    df2 = df2.merge(df1, on='id')
    df2 = df2.merge(df3, on='id')
    del df1
    del df3
    df2 = df2.sort_values('vote_count', ascending=False).drop_duplicates('id').sort_index()
    #m = df2['vote_count'].quantile(0.9)
    #df2 = df2.copy().loc[df2['vote_count'] >= m]
    #df2 = df2.reset_index()

    features = ['cast', 'crew', 'keywords', 'genres']
    for feature in features:
        df2[feature] = df2[feature].apply(literal_eval)
    # Define new director, cast, genres and keywords features that are in a suitable form.
    df2['director'] = df2['crew'].apply(get_director)
    df2['genres'] = df2['genres'].apply(get_list_g)

    features = ['cast', 'keywords']
    for feature in features:
        df2[feature] = df2[feature].apply(get_list)

    # Apply clean_data function to your features.
    features = ['cast', 'keywords', 'director', 'genres']

    for feature in features:
        df2[feature+"1"] = df2[feature]

        df2[feature] = df2[feature].apply(clean_data)
    df2['soup'] = df2.apply(create_soup, axis=1)
    return df2


def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])


# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        # Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


# Returns the list top l elements or entire list; whichever is more.
def get_list(x, l=5):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        # Check if more than l elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > l:
            names = names[:l]
        return names

    # Return empty list in case of missing/malformed data
    return []


# Returns the list top l elements or entire list; whichever is more.
def get_list_g(x, l=2):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        # Check if more than l elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > l:
            names = names[:l]
        return names

    # Return empty list in case of missing/malformed data
    return []


def popularity(data, n=10):
    #data['score'] = data.apply(weighted_rating, axis=1)
    data = data.sort_values('score', ascending=False)
    return data

def get_list_id_moviest():
	global list_id_movies
	return list_id_movies
def popularity_get_recommendations(data, n=10):
    return data[['title', 'vote_count', 'vote_average', 'score']].head(n + 1)

icb=""
ucb=""
n=""
user_data=""


def get_user_data():
    global user_data
    return user_data
def get_n():
    global n
    return n
def get_icb():
    global icb
    return icb
def get_ucb():
    global ucb
    return ucb

def get_item_vector():
    global item_vector
    return item_vector

def get_data(movieID):
    global data
    a= data.loc[data["id"] == int(movieID)]
    return a[['id','imdb_id','title','cast1','director1','keywords1','poster_path','overview','genres1','release_date']].iloc[0]


def get_all_movies():
    global data
    return data[['id','title']].sort_values(by=['title'])

def init():
    print("hello")
    global icb
    global ucb
    global n
    global user_data
    global data
    global list_id_movies
    global item_vector

    df2 = pd.read_csv("static/meta_data_4852.csv")
    df1 = pd.read_csv("static/credits.csv")
    df3 = pd.read_csv("static/keywords.csv")
    item_vector = pd.read_csv("static/MF_Model/item_vector.csv")
    item_vector['numpy_vec']=item_vector.vector.apply(lambda x: np.fromstring(x, dtype=np.float ,sep=','))

	#dorin:change
    #ratings = pd.read_csv("data/rating_5.7M.csv")
    #list_id_movies = ratings['id'].unique()
    #print(len(list_id_movies))
	
    moviesLink = pd.read_csv('static/item2id.csv', header=None,names=['origId', 'newId'])
    list_id_movies = moviesLink['origId'].to_list()
	
	
	
    #ratings = ratings.rename(columns={'movieId': 'id'})
    
    data = prepare_data(df1, df2, df3)
    del (df1, df2, df3)
    m = data['vote_count'].quantile(0.9)
    C = data['vote_average'].mean()
    n = 10
    #icb = item_content_base(data)
    #ucb = user_content_base(data)


    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * C)
    # popular= popularity(data)
    # print(popularity_get_recommendations(popular,n))
	
    print("done")
