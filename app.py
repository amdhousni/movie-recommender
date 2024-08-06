import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# Load the movie data
df_movies = pd.read_csv('movies.csv')

# Set the title of the app
st.title('Movie Recommender System')

# Add a text input field in the sidebar
movie_title = st.sidebar.text_input("Titre du film")

# Filter the dataframe to get the row where the `title` column matches the `movie_title`
selected_movie = df_movies[df_movies['title'] == movie_title]


def get_recommendations(movie_title, df_movies, num_recommendations=10):
    """
    This function takes a movie title and a DataFrame of movies and returns a list of recommended movie titles based on fuzzy string matching.
    """
    # Calculate similarity scores for all movies in the dataframe
    df_movies['similarity_score'] = df_movies['title'].apply(
        lambda x: fuzz.ratio(x, movie_title)
    )

    # Sort movies by similarity score in descending order
    sorted_movies = df_movies.sort_values(by='similarity_score', ascending=False)

    # Get the top N most similar movies (excluding the input movie itself)
    recommended_movies = sorted_movies[sorted_movies['title'] != movie_title].head(
        num_recommendations
    )

    return recommended_movies[['title', 'language', 'country']]

if not selected_movie.empty:

    recommendations = get_recommendations(movie_title, df_movies)

    if not recommendations.empty:
        # Display recommended movies
        st.header('Films recommandés')
        st.write(recommendations.to_markdown(index=False, numalign="left", stralign="left"))

    else:
        st.write("Aucun film recommandé trouvé pour ce titre.")

else:
    st.write("Veuillez entrer un titre de film valide.")
