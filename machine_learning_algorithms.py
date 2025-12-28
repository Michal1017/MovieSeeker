import apicalls
from math import sqrt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings("ignore")

def RecommendSimilarMovies(index):
    movieList = apicalls.GetMoviesFromJson(False)

    movieList = movieList.drop_duplicates(subset=['title', 'release_date'])

    movieList['release_year'] = movieList['release_date'].str.extract(
    r'([0-9]{4})', expand=True).astype(float)

    movieList.dropna(inplace=True)

    movieList['release_year'] = movieList['release_year'].astype(int)

    genresDict = apicalls.GetMovieGenres()

    movieList['genres'] = movieList['genre_ids'].apply(lambda x: ' '.join([genresDict[i] for i in x]))

    movieList['mixed_data'] = movieList["genres"] + " " + movieList["original_language"] + \
                             movieList["overview"]
    
    movieList = movieList.reset_index()
    indices = pd.Series(movieList.index, index=movieList['id'])

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(movieList['mixed_data'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    index_of_movie = indices[index]

    similarities = list(enumerate(cosine_sim[index_of_movie]))

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    similarities = similarities[1:31]

    movieList['vote_count_norm'] = MinMaxScaler().fit_transform(
        np.array(movieList['vote_count']).reshape(-1, 1))
    movieList['popularity_norm'] = MinMaxScaler().fit_transform(
        np.array(movieList['popularity']).reshape(-1, 1))
    movieList['vote_average_norm'] = MinMaxScaler().fit_transform(
        np.array(movieList['vote_average']).reshape(-1, 1))
    movieList['release_year_norm'] = MinMaxScaler().fit_transform(
        np.array(movieList['release_year']).reshape(-1, 1))
    
    recommend_movie_indices = [i[0] for i in similarities]

    euclidian_distance = []
    for i in recommend_movie_indices:
        distance = sqrt((movieList['vote_count_norm'][index_of_movie]-movieList['vote_count_norm'][i])**2+(movieList['popularity_norm'][index_of_movie] -
                        movieList['popularity_norm'][i])**2+(movieList['vote_average_norm'][index_of_movie]-movieList['vote_average_norm'][i])**2 + 
                        (movieList['release_year_norm'][index_of_movie]-movieList['release_year_norm'][i])**2)
        euclidian_distance.append((i, distance))

    euclidian_distance = sorted(euclidian_distance, key=lambda x: x[1])

    # get top most similiar movies
    euclidian_distance = euclidian_distance[1:21]

    # get indices of most similiar movies
    recommend_movie_indices = [i[0] for i in euclidian_distance]

    recommend_movie = movieList.iloc[recommend_movie_indices]

    resultList = pd.DataFrame(recommend_movie)[['title', 'poster_path', 'vote_average','id']]

    resultList['poster_path'] = 'https://image.tmdb.org/t/p/w500' + resultList['poster_path']

    return resultList


