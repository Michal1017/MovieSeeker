import requests
import tmdbsimple as tmdb
import pandas as pd

def GetApiKey(path):
    f = open(path, 'r')
    API_KEY = f.read()
    return API_KEY


def GetMostPopularFilmsList():
    apiKey = GetApiKey('C:/Users/micha/.secret/tMDb_API.txt')
    filmList = []
    url = 'https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&offset=20&page=1&api_key='
    req = requests.get(url+apiKey).json()
    results = req['results']
    filmList.extend(results)
    resultList = pd.DataFrame(filmList)[['original_title', 'poster_path', 'vote_average']]
    resultList['poster_path'] = 'https://image.tmdb.org/t/p/w500' + resultList['poster_path']
    return resultList

# result = GetMostPopularFilmsList()

# for i, row in result.iterrows():
#     print(row['poster_path'])