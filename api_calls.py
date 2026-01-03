import json
import requests
import pandas as pd
import os
import time
import flet as ft
from datetime import datetime


def get_api_key(path):
    f = open(path, "r")
    API_KEY = f.read()
    return API_KEY


def get_most_popular_movies_list():
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    movie_list = []
    url = "https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&page=1&api_key="
    req = requests.get(url + apiKey).json()
    results = req["results"]
    movie_list.extend(results)
    resultList = pd.DataFrame(movie_list)[
        ["title", "poster_path", "vote_average", "id"]
    ]
    resultList["poster_path"] = (
        "https://image.tmdb.org/t/p/w500" + resultList["poster_path"]
    )
    return resultList


def get_specific_movie(id):
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key="
    req = requests.get(url + apiKey).json()
    req["poster_path"] = "https://image.tmdb.org/t/p/w500" + req["poster_path"]
    return req


def movie_list_by_title(title):
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    url = (
        "https://api.themoviedb.org/3/search/movie?api_key="
        + apiKey
        + "&query="
        + title
    )
    req = requests.get(url).json()
    results = req["results"]
    movie_list = []
    movie_list.extend(results)
    resultList = pd.DataFrame()
    if not movie_list:
        return resultList
    resultList[["title", "poster_path", "release_date", "id"]] = pd.DataFrame(
        movie_list
    )[["title", "poster_path", "release_date", "id"]]
    resultList["release_date"] = resultList["release_date"].str[:4]
    resultList["poster_path"] = (
        "https://image.tmdb.org/t/p/w500" + resultList["poster_path"]
    )
    return resultList


def get_movie_list():
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")

    finallist = []
    n = 0
    while n < 500:
        n += 1
        url = "https://api.themoviedb.org/3/discover/movie?&sort_by=popularity.desc&offset=20&page={}&api_key=".format(
            n
        )
        req = requests.get(url + apiKey).json()
        results = req["results"]
        finallist.extend(results)

    with open("movie_data.json", "w") as file:
        json.dump(finallist, file)


def get_movies_from_json(shouldUpdate):
    if shouldUpdate:
        get_movie_list()
        with open("movie_data.json", "r") as file:
            movies = json.load(file)
    else:
        with open("movie_data.json", "r") as file:
            movies = json.load(file)

    movies = pd.DataFrame(movies)[
        [
            "title",
            "adult",
            "genre_ids",
            "id",
            "original_language",
            "overview",
            "popularity",
            "poster_path",
            "release_date",
            "vote_average",
            "vote_count",
        ]
    ]

    return movies


def get_movie_genres():
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en&api_key="
    req = requests.get(url + apiKey).json()
    results = req["genres"]
    genresDict = {}
    for el in results:
        genresDict[el["id"]] = el["name"]

    return genresDict


def measure_time(func):
    start_time = time.time()  # Start the timer
    result = func()  # Call the function
    end_time = time.time()  # End the timer
    execution_time = end_time - start_time
    return result, execution_time


# result, execution_time = measure_time(get_movie_list)
# movies = []
# with open("movie_data.json", "r") as file:
#     movies = json.load(result)
# print(f"Execution time: {execution_time} seconds")
# print(f"Number of movies: {len(movies)}")


def is_int_textfield(tf):
    if not tf.value:
        return False
    try:
        int(tf.value)
        return True
    except ValueError:
        return False


def find_movie_with_filters(from_year, to_year, min_time, max_time):
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    movie_list = []
    url = "https://api.themoviedb.org/3/discover/movie?language=en-US&page=1&sort_by=popularity.desc"
    current_year = datetime.now().year
    if (
        is_int_textfield(from_year)
        and int(from_year.value) >= 1888
        and int(from_year.value) <= current_year
    ):
        url = url + f"&primary_release_date.gte={from_year.value}-01-01"
    if (
        is_int_textfield(to_year)
        and int(to_year.value) >= 1888
        and int(to_year.value) <= current_year
        and int(to_year.value) >= int(from_year.value)
    ):
        url = url + f"&primary_release_date.lte={to_year.value}-12-31"
    if is_int_textfield(min_time) and int(min_time.value) > 0:
        url = url + f"&with_runtime.gte={min_time.value}"
    if (
        is_int_textfield(max_time)
        and int(max_time.value) > 0
        and int(max_time.value) >= int(min_time.value)
    ):
        url = url + f"&with_runtime.lte={max_time.value}"

    url = url + "&api_key=" + apiKey
    req = requests.get(url).json()
    results = req["results"]
    movie_list.extend(results)
    resultList = pd.DataFrame(movie_list)[["title", "poster_path", "id"]]
    resultList["poster_path"] = (
        "https://image.tmdb.org/t/p/w500" + resultList["poster_path"]
    )

    if not resultList.empty:
        return resultList.sample(1).iloc[0]
    else:
        return "Empty result"
