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
    # ... (logique pour trouver des films similaires en utilisant cosine_sim)

# Interface Streamlit
st.title('Movie Recommender')
selected_movie = st.selectbox('Select a movie:', df['primaryTitle'].values)

if st.button('Get Recommendations'):
    recommendations = get_recommendations(selected_movie)
    st.write('Recommended movies:')
    for movie in recommendations:
        st.write(movie)
