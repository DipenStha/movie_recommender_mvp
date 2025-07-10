import pandas as pd

def load_data():
    ratings = pd.read_csv(
        'https://files.grouplens.org/datasets/movielens/ml-100k/u.data',
        sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp']
    )
    movies = pd.read_csv(
        'https://files.grouplens.org/datasets/movielens/ml-100k/u.item',
        sep='|', encoding='latin-1', header=None, usecols=[0,1], names=['movie_id', 'title']
    )
    ratings = ratings.merge(movies, on='movie_id')
    return ratings
