import numpy as np

import pandas as pd

from rsAPI.init_data import get_item_vector


def get_MF_movies_top(u_rat, n):
    item_vector=get_item_vector()
    items =  item_vector[item_vector['movieId'].isin(u_rat)]
    items = items['vector'].apply(lambda x: pd.Series(str(x).split(",")))
    items=items.apply(pd.to_numeric)         
    maxCol=lambda x: max(x.min(), x.max(), key=abs)
    user_vec = items.apply(maxCol,axis=0).to_numpy()

    item_vector['grade'] = item_vector['numpy_vec'].apply(lambda x: np.dot(x,user_vec))
    item_vector['final_grade'] =item_vector['grade']+item_vector['bias']
    item_vector = item_vector.sort_values(by=['final_grade'], ascending=False)
    item_vector= item_vector['movieId'].head(n)
    top_n = item_vector.tolist()
    top_n = [int(i) for i in top_n]  

    return  top_n
	