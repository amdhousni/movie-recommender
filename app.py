import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Charger les données
df = pd.read_csv('movies.csv')

# Prétraitement des données (encoder les genres)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['genres'])

# Calculer la similarité entre les films
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Fonction pour obtenir des recommandations
def get_recommendations(title, cosine_sim=cosine_sim):
    # Find the index of the movie that matches the title
    idx = df[df['primaryTitle'] == title].index[0]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['primaryTitle'].iloc[movie_indices]


# Interface Streamlit
st.title('Movie Recommender')
selected_movie = st.selectbox('Select a movie:', df['primaryTitle'].values)

if st.button('Get Recommendations'):
    recommendations = get_recommendations(selected_movie)
    st.write('Recommended movies:')
    for movie in recommendations:
        st.write(movie)
