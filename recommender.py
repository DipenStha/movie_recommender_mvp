import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def build_similarity_matrix(ratings):
    user_movie_matrix = ratings.pivot_table(index='user_id', columns='title', values='rating')
    similarity = cosine_similarity(user_movie_matrix.T.fillna(0))
    sim_df = pd.DataFrame(similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)
    return sim_df

def recommend(movie_title, sim_df, num_recommendations=5):
    if movie_title not in sim_df:
        return []
    sim_scores = sim_df[movie_title].sort_values(ascending=False)[1:num_recommendations+1]
    return sim_scores
