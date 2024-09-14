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
    filmList = apicalls.GetFilmsFromJson()

    filmList = filmList.drop_duplicates(subset=['title', 'release_date'])

    filmList['release_year'] = filmList['release_date'].str.extract(
    r'([0-9]{4})', expand=True).astype(float)

    filmList.dropna(inplace=True)

    filmList['release_year'] = filmList['release_year'].astype(int)

    genresDict = apicalls.GetMovieGenres()

    filmList['genres'] = filmList['genre_ids'].apply(lambda x: ' '.join([genresDict[i] for i in x]))

    print(filmList.info())

    filmList['mixed_data'] = filmList["genres"] + " " + filmList["original_language"] + \
                             filmList["overview"]
    
    filmList = filmList.reset_index()
    indices = pd.Series(filmList.index, index=filmList['id'])

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(filmList['mixed_data'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    index_of_movie = indices[index]

    similarities = list(enumerate(cosine_sim[index_of_movie]))

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    similarities = similarities[1:31]

    filmList['vote_count_norm'] = MinMaxScaler().fit_transform(
        np.array(filmList['vote_count']).reshape(-1, 1))
    filmList['popularity_norm'] = MinMaxScaler().fit_transform(
        np.array(filmList['popularity']).reshape(-1, 1))
    filmList['vote_average_norm'] = MinMaxScaler().fit_transform(
        np.array(filmList['vote_average']).reshape(-1, 1))
    filmList['release_year_norm'] = MinMaxScaler().fit_transform(
        np.array(filmList['release_year']).reshape(-1, 1))
    
    recommend_movie_indices = [i[0] for i in similarities]

    euclidian_distance = []
    for i in recommend_movie_indices:
        distance = sqrt((filmList['vote_count_norm'][index_of_movie]-filmList['vote_count_norm'][i])**2+(filmList['popularity_norm'][index_of_movie] -
                        filmList['popularity_norm'][i])**2+(filmList['vote_average_norm'][index_of_movie]-filmList['vote_average_norm'][i])**2 + 
                        (filmList['release_year_norm'][index_of_movie]-filmList['release_year_norm'][i])**2)
        euclidian_distance.append((i, distance))

    euclidian_distance = sorted(euclidian_distance, key=lambda x: x[1])

    # get top most similiar movies
    euclidian_distance = euclidian_distance[1:11]

    # get indices of most similiar movies
    recommend_movie_indices = [i[0] for i in euclidian_distance]

    recommend_movie = filmList.iloc[recommend_movie_indices]

    print(recommend_movie['title'])



RecommendSimilarMovies(155)

