import streamlit as st
import pandas as pd

# Load the movie data
df_movies = pd.read_csv('movies.csv')

# Set the title of the app
st.title('Movie Recommender System')

# Count the occurrences of each movie
movie_counts = df_movies['title'].value_counts()

# Sort the movie counts in descending order and get the top 10
top_movies = movie_counts.head(10)

# Display the top 10 most popular movies
st.header('Most Popular Movies')
st.write(top_movies.to_markdown(numalign="left", stralign="left"))
