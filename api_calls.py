import json
import requests
import pandas as pd
import os
import time
import flet as ft
from datetime import datetime
from models.movies_filters import MoviesFilters


def get_api_key(path):
    f = open(path, "r")
    API_KEY = f.read()
    return API_KEY


def full_poster_path(path):
    if pd.isna(path):
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8u_kGMjMWclIFDsOJpohPnMVS1cuFf7Kvcg&s"
    else:
        return "https://image.tmdb.org/t/p/w500" + path


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
    resultList["poster_path"] = resultList["poster_path"].apply(full_poster_path)
    return resultList


def get_specific_movie(id):
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key="
    req = requests.get(url + apiKey).json()
    if pd.isna(req["poster_path"]):
        req["poster_path"] = (
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8u_kGMjMWclIFDsOJpohPnMVS1cuFf7Kvcg&s"
        )
    else:
        req["poster_path"] = "https://image.tmdb.org/t/p/w500" + req["poster_path"]
    return req


def get_specific_movie_for_finding_similar_movies_algorithm(id):
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key="
    req = requests.get(url + apiKey).json()
    keys = (
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
    )

    return {k: req[k] for k in keys if k in req}


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


def is_float_textfield(tf):
    if not tf.value:
        return False
    try:
        float(tf.value)
        return True
    except ValueError:
        return False


def find_movie_with_filters(movie_filters):
    apiKey = get_api_key("C:/Users/micha/.secret/tMDb_API.txt")
    movie_list = []
    url = "https://api.themoviedb.org/3/discover/movie?language=en-US&page=1&sort_by=popularity.desc"
    current_year = datetime.now().year
    if (
        is_int_textfield(movie_filters.from_year)
        and int(movie_filters.from_year.value) >= 1888
        and int(movie_filters.from_year.value) <= current_year
    ):
        url = url + f"&primary_release_date.gte={movie_filters.from_year.value}-01-01"
    if (
        is_int_textfield(movie_filters.to_year)
        and int(movie_filters.to_year.value) >= 1888
        and int(movie_filters.to_year.value) <= current_year
        and (
            not is_int_textfield(movie_filters.from_year)
            or int(movie_filters.to_year.value) >= int(movie_filters.from_year.value)
        )
    ):
        url = url + f"&primary_release_date.lte={movie_filters.to_year.value}-12-31"
    if (
        is_int_textfield(movie_filters.min_time)
        and int(movie_filters.min_time.value) > 0
    ):
        url = url + f"&with_runtime.gte={movie_filters.min_time.value}"
    if (
        is_int_textfield(movie_filters.max_time)
        and int(movie_filters.max_time.value) > 0
        and (
            not is_int_textfield(movie_filters.min_time)
            or int(movie_filters.max_time.value) >= int(movie_filters.min_time.value)
        )
    ):
        url = url + f"&with_runtime.lte={movie_filters.max_time.value}"
    if (
        is_float_textfield(movie_filters.min_rating)
        and float(movie_filters.min_rating.value) >= 0
        and float(movie_filters.min_rating.value) <= 10
    ):
        url = url + f"&vote_average.gte={movie_filters.min_rating.value}"
    if (
        is_float_textfield(movie_filters.max_rating)
        and float(movie_filters.max_rating.value) >= 0
        and float(movie_filters.max_rating.value) <= 10
        and (
            not is_float_textfield(movie_filters.min_rating)
            or float(movie_filters.max_rating.value)
            >= float(movie_filters.min_rating.value)
        )
    ):
        url = url + f"&vote_average.lte={movie_filters.max_rating.value}"

    choosed_genres = [cb.label for cb in movie_filters.genres if cb.value]

    if choosed_genres:
        all_genres = get_movie_genres()
        checked_keys = [
            key for key, value in all_genres.items() if value in choosed_genres
        ]
        url = url + "&with_genres="
        for i, value in enumerate(checked_keys):
            if i == len(checked_keys) - 1:
                url = url + f"{value}"
            else:
                url = url + f"{value},"

    choosed_unwanted_genres = [
        cb.label for cb in movie_filters.unwanted_genres if cb.value
    ]

    if choosed_unwanted_genres:
        all_genres = get_movie_genres()
        checked_keys = [
            key for key, value in all_genres.items() if value in choosed_unwanted_genres
        ]
        url = url + "&without_genres="
        for i, value in enumerate(checked_keys):
            if i == len(checked_keys) - 1:
                url = url + f"{value}"
            else:
                url = url + f"{value},"

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
