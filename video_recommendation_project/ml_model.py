import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_videos(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch interactions
    query = '''
    SELECT user_id, video_id, action
    FROM interactions
    '''
    data = pd.read_sql_query(query, conn)
    conn.close()

    if data.empty:
        return []

    # Create a pivot table
    pivot_table = data.pivot_table(index='user_id', columns='video_id', aggfunc='size', fill_value=0)

    # Compute similarity
    similarity_matrix = cosine_similarity(pivot_table)

    # Get user index
    user_index = pivot_table.index.get_loc(user_id)

    # Recommend based on similar users
    similar_users = similarity_matrix[user_index]
    recommended_videos = []

    for i, score in enumerate(similar_users):
        if i != user_index:
            recommended_videos.extend(pivot_table.iloc[i].index.tolist())

    return list(set(recommended_videos))
