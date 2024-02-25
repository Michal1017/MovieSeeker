import json
import requests
import pandas as pd
import os

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

def MovieListByTitle(title):
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    url = 'https://api.themoviedb.org/3/search/movie?api_key='+apiKey+"&query="+title
    req = requests.get(url).json()
    results = req['results']
    filmList = []
    filmList.extend(results)
    resultList = pd.DataFrame()
    if not filmList:
        return resultList
    resultList[['title', 'poster_path', 'release_date', 'id']] = pd.DataFrame(filmList)[['title', 'poster_path', 'release_date', 'id']]
    resultList['release_date'] = resultList['release_date'].str[:4]
    resultList['poster_path'] = 'https://image.tmdb.org/t/p/w500' + resultList['poster_path']
    return resultList

def GetFilmList():
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')

    finallist = []
    n = 0
    while n < 500:
        n += 1
        url = 'https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&offset=20&page={}&api_key='.format(n)
        req = requests.get(url+apiKey).json()
        results = req['results']
        finallist.extend(results)

    with open("film_data.json", "w") as file:
        json.dump(finallist, file)

def GetFilmsFromJson():
    if os.path.exists("film_data.json"):
        with open("film_data.json", "r") as file:
            films = json.load(file)
    else:
        GetFilmList()
        with open("film_data.json", "r") as file:
            films = json.load(file)

    films = pd.DataFrame(films)[['title','adult','genre_ids','id','original_language','overview','popularity','poster_path','release_date','vote_average','vote_count']]

    print(films.columns)
