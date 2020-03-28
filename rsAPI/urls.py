from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('getMovieDetails', views.getMovieDetails, name='getMovieDetails'),
    path('getAllMovies', views.getAllMovies, name='getAllMovies'),
	path('getRecommendation', views.getRecommendation, name='getRecommendation'),


]