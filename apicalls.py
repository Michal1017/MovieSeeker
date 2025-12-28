import json
import requests
import pandas as pd
import os
import time

def GetApiKey(path):
    f = open(path, 'r')
    API_KEY = f.read()
    return API_KEY


def GetMostPopularMoviesList():
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    movieList = []
    url = 'https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&page=1&api_key='
    req = requests.get(url+apiKey).json()
    results = req['results']
    movieList.extend(results)
    resultList = pd.DataFrame(movieList)[['title', 'poster_path', 'vote_average','id']]
    resultList['poster_path'] = 'https://image.tmdb.org/t/p/w500' + resultList['poster_path']
    return resultList

def GetSpecificMovie(id):
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    url = 'https://api.themoviedb.org/3/movie/'+str(id)+"?api_key="
    req = requests.get(url+apiKey).json()
    req['poster_path'] = 'https://image.tmdb.org/t/p/w500' + req['poster_path']
    return req

def MovieListByTitle(title):
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    url = 'https://api.themoviedb.org/3/search/movie?api_key='+apiKey+"&query="+title
    req = requests.get(url).json()
    results = req['results']
    movieList = []
    movieList.extend(results)
    resultList = pd.DataFrame()
    if not movieList:
        return resultList
    resultList[['title', 'poster_path', 'release_date', 'id']] = pd.DataFrame(movieList)[['title', 'poster_path', 'release_date', 'id']]
    resultList['release_date'] = resultList['release_date'].str[:4]
    resultList['poster_path'] = 'https://image.tmdb.org/t/p/w500' + resultList['poster_path']
    return resultList

def GetMovieList():
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')

    finallist = []
    n = 0
    while n < 500:
        n += 1
        url = 'https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&offset=20&page={}&api_key='.format(n)
        req = requests.get(url+apiKey).json()
        results = req['results']
        finallist.extend(results)

    with open("movie_data.json", "w") as file:
        json.dump(finallist, file)

def GetMoviesFromJson(shouldUpdate):
    if shouldUpdate:
        GetMovieList()
        with open("movie_data.json", "r") as file:
            movies = json.load(file)
    else:
        with open("movie_data.json", "r") as file:
            movies = json.load(file)

    movies = pd.DataFrame(movies)[['title','adult','genre_ids','id','original_language','overview','popularity','poster_path','release_date','vote_average','vote_count']]

    return movies

def GetMovieGenres():
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en&api_key="
    req = requests.get(url+apiKey).json()
    results = req['genres']
    genresDict = {}
    for el in results:
        genresDict[el['id']] = el['name']
    
    return genresDict

def measure_time(func):
    start_time = time.time()  # Start the timer
    result = func()           # Call the function
    end_time = time.time()    # End the timer
    execution_time = end_time - start_time
    return result, execution_time

# result, execution_time = measure_time(GetMovieList)
# movies = []
# with open("movie_data.json", "r") as file:
#     movies = json.load(result)
# print(f"Execution time: {execution_time} seconds")
# print(f"Number of movies: {len(movies)}")