from django.shortcuts import render
from django.http import HttpResponse
from rsAPI.init_data import get_icb,get_ucb,get_user_data,get_n,get_data ,get_all_movies
from rsAPI.MF import get_MF_movies_top
from rsAPI.loadAEModel import get_AE_top
from rsAPI.init_data import get_list_id_moviest
import json
import random
sys_random = random.SystemRandom()
def getRecommendation(request):
	dicExplanations={}
	movieAE =[]
	movieMF=[]
	exaplanation={}
	exaplanation[1]="CB - item - item: The movie overview is similar to other movie you liked"
	exaplanation[2]="CB - item - item: The movie feauters(cast, geners, director) are similar to other movie you liked"
	exaplanation[3]="CB - item - user: Based on your favourite actors and directors"
	exaplanation[4]="popolarity: The movie is popular"
	exaplanation[5]= "CF item - user : Other users with similar movie ratings to you liked this movie"
	exaplanation[6]= "CF item - item : ratings to you liked this movie"
	exaplanation[7]="The attributed we calculated automatically for the movie match the attributes we calculated automatically for you"
	
	list_id_moviest=get_list_id_moviest()
	
	movie_list = request.GET.get('movie_list','')
	movie_list = movie_list.split(',')
	movie_list= list(map(int, movie_list))
	#print(movie_list)
	ratings_lis = request.GET.get('ratings_lis','')
	ratings_lis = ratings_lis.split(',')
	ratings_lis= list(map(int, ratings_lis))


	dicData={}
	d = get_all_movies()
	d = d.sample(n=18)
	i=0

		
	movieMF  = get_MF_movies_top(movie_list,9)
	movieAE=get_AE_top(movie_list,9)
	return HttpResponse(json.dumps([movieAE,movieMF,exaplanation]))

	
def getMovieDetails(request):
    movieID = request.GET.get('mID','')
    data = get_data(movieID)
    return HttpResponse(data.to_json())

def getAllMovies(request):
    d = get_all_movies()
    d = dict(zip(d.id, d.title))
    return HttpResponse(json.dumps(d))

def index(request):
    user = request.GET.get('user','')
    print(user)
    predict_explain()
    result='{"data":[1,3,6,8]}'
    return HttpResponse(result)


def predict_explain():
    icb = get_icb()
    ucb=get_ucb()
    user_data = get_user_data()
    n = get_n()
    movies = [  # 'The Godfather'
        'The Dark Knight Rises']  # ,'The Avengers' ]
    for movie in movies:
        # print(icb.get_recommendations(movie,'overview',n))
        rec, sim, x, y = icb.get_recommendations(movie, 'features', n)
        print(rec)
    print(ucb.get_recommendations(user_data, icb, n))

