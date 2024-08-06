import streamlit as st
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
df_movies = pd.read_csv('movies.csv')

# Set the title of the app
st.title('Movie Recommender System')

# Add a text input field in the sidebar
movie_title = st.sidebar.text_input("Titre du film")

# Filter the dataframe to get the row where the `title` column matches the `movie_title`
selected_movie = df_movies[df_movies['title'] == movie_title]

# Extract the genres from the selected movie
if not selected_movie.empty:
    movie_genres = selected_movie['genres'].iloc[0].split(',')

    # Create a new column `genre_match`
    df_movies['genre_match'] = df_movies['genres'].astype(str).str.contains('|'.join(movie_genres), case=False)

    # Filter the dataframe to keep only the rows where `genre_match` is True
    recommended_movies = df_movies[df_movies['genre_match']]

    if not recommended_movies.empty:
        # Display the genres of the selected movie
        st.write(f"Genres du film sélectionné : {', '.join(movie_genres)}")

        # Sample 10 movies from the recommended movies and display them
        st.write(recommended_movies.sample(10)[['title', 'genres', 'language', 'country']].to_markdown(index=False, numalign="left", stralign="left"))

    else:
        st.write("Aucun film recommandé trouvé pour ces genres.")

else:
    st.write("Veuillez entrer un titre de film valide.")
