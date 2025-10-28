import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import sys

# Load dataset
data = pd.read_csv('tcc_ceds_music.csv')

# Precompute TF-IDF on combined features (genre + artist + track + lyrics)
data['combined_features'] = (
        data['genre'].fillna('') + ' ' +
        data['artist_name'].fillna('') + ' ' +
        data['track_name'].fillna('') + ' ' +
        data['lyrics'].fillna('')
)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(artist, genres, top_n=10):
    # Filter by artist (partial match) and genres
    mask = data['artist_name'].str.lower().str.contains(artist.lower())
    if genres:
        genre_mask = data['genre'].isin(genres)
        mask = mask & genre_mask
    filtered_indices = data[mask].index

    if len(filtered_indices) == 0:
        return []  # No matches

    # Mean similarity from filtered songs
    sim_scores = cosine_sim[filtered_indices].mean(axis=0)
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:top_n]
    song_indices = [i[0] for i in sim_scores]

    # Return relevant fields (adapt to your Music model)
    recommendations = data.iloc[song_indices][['track_name', 'artist_name', 'release_date', 'genre', 'lyrics']].to_dict(orient='records')
    return recommendations

if __name__ == "__main__":
    # Read input file from Flutter
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.json'
    with open(input_file, 'r') as f:
        input_data = json.load(f)
    artist = input_data.get('artist', '')
    genres = input_data.get('genres', [])

    # Compute
    recs = get_recommendations(artist, genres)

    # Write output
    output_file = 'output.json'
    with open(output_file, 'w') as f:
        json.dump({'recommendations': recs}, f)