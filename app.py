import streamlit as st
import pandas as pd

# Load the movie data
df_movies = pd.read_csv('movies.csv')

# Set the title of the app
st.title('Movie Recommender System')

# Display the top 10 most popular movies
st.header('Most Popular Movies')
top_movies = df_movies.sort_values(by='popularity', ascending=False).head(10)
st.write(top_movies[['primaryTitle', 'genres', 'popularity', 'tmdbRating']].to_markdown(index=False, numalign="left", stralign="left"))
