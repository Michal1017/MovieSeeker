import requests
import pandas as pd

def GetApiKey(path):
    f = open(path, 'r')
    API_KEY = f.read()
    return API_KEY


def GetMostPopularFilmsList():
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    filmList = []
    url = 'https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&page=1&api_key='
    req = requests.get(url+apiKey).json()
    results = req['results']
    filmList.extend(results)
    resultList = pd.DataFrame(filmList)[['title', 'poster_path', 'vote_average','id']]
    resultList['poster_path'] = 'https://image.tmdb.org/t/p/w500' + resultList['poster_path']
    return resultList

def GetSpecificMovie(id):
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    url = 'https://api.themoviedb.org/3/movie/'+str(id)+"?api_key="
    req = requests.get(url+apiKey).json()
    req['poster_path'] = 'https://image.tmdb.org/t/p/w500' + req['poster_path']
    return req
