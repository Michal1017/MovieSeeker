import api_calls
from math import sqrt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import warnings
from collections import Counter

warnings.filterwarnings("ignore")


def recommend_similar_movies(index):
    movie_list = api_calls.get_movies_from_json(False)

    if index not in movie_list["id"].values:
        movie_list = pd.concat(
            [movie_list, pd.DataFrame([api_calls.get_specific_movie(index)])]
        )

    movie_list = movie_list.drop_duplicates(subset=["title", "release_date"])

    movie_list["release_year"] = (
        movie_list["release_date"].str.extract(r"([0-9]{4})", expand=True).astype(float)
    )

    most_common_release_year = movie_list["release_year"].mode()[0]
    movie_list["release_year"].fillna(most_common_release_year, inplace=True)

    movie_list["release_year"] = movie_list["release_year"].astype(int)

    genresDict = api_calls.get_movie_genres()

    genre_lists = [x for x in movie_list["genre_ids"] if isinstance(x, list)]
    most_common_genres = Counter(tuple(x) for x in genre_lists).most_common(1)[0][0]
    most_common_genres = list(most_common_genres)

    movie_list["genre_ids"] = movie_list["genre_ids"].apply(
        lambda x: most_common_genres if not isinstance(x, list) else x
    )

    movie_list["genres"] = movie_list["genre_ids"].apply(
        lambda x: " ".join([genresDict[i] for i in x])
    )

    movie_list["mixed_data"] = (
        movie_list["genres"]
        + " "
        + movie_list["original_language"]
        + movie_list["overview"]
    )

    movie_list = movie_list.reset_index(drop=True)
    indices = pd.Series(movie_list.index, index=movie_list["id"])

    count = CountVectorizer(stop_words="english")
    count_matrix = count.fit_transform(movie_list["mixed_data"])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    index_of_movie = indices[index]

    similarities = list(enumerate(cosine_sim[index_of_movie]))

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    similarities = similarities[1:31]

    movie_list["vote_count_norm"] = MinMaxScaler().fit_transform(
        np.array(movie_list["vote_count"]).reshape(-1, 1)
    )
    movie_list["popularity_norm"] = MinMaxScaler().fit_transform(
        np.array(movie_list["popularity"]).reshape(-1, 1)
    )
    movie_list["vote_average_norm"] = MinMaxScaler().fit_transform(
        np.array(movie_list["vote_average"]).reshape(-1, 1)
    )
    movie_list["release_year_norm"] = MinMaxScaler().fit_transform(
        np.array(movie_list["release_year"]).reshape(-1, 1)
    )

    recommend_movie_indices = [i[0] for i in similarities]

    euclidian_distance = []
    for i in recommend_movie_indices:
        distance = sqrt(
            (
                movie_list["vote_count_norm"][index_of_movie]
                - movie_list["vote_count_norm"][i]
            )
            ** 2
            + (
                movie_list["popularity_norm"][index_of_movie]
                - movie_list["popularity_norm"][i]
            )
            ** 2
            + (
                movie_list["vote_average_norm"][index_of_movie]
                - movie_list["vote_average_norm"][i]
            )
            ** 2
            + (
                movie_list["release_year_norm"][index_of_movie]
                - movie_list["release_year_norm"][i]
            )
            ** 2
        )
        euclidian_distance.append((i, distance))

    euclidian_distance = sorted(euclidian_distance, key=lambda x: x[1])

    # get top most similiar movies
    euclidian_distance = euclidian_distance[1:21]

    # get indices of most similiar movies
    recommend_movie_indices = [i[0] for i in euclidian_distance]

    recommend_movie = movie_list.iloc[recommend_movie_indices]

    resultList = pd.DataFrame(recommend_movie)[
        ["title", "poster_path", "vote_average", "id"]
    ]

    resultList["poster_path"] = resultList["poster_path"].apply(
        api_calls.full_poster_path
    )

    return resultList
