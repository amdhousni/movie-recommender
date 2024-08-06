import streamlit as st
import pandas as pd

# Charger les données du film
df_movies = pd.read_csv('movies.csv')

# Définir le titre de l'application
st.title('Système de Recommandation de Films')

# Créer une barre latérale pour les filtres
st.sidebar.header('Filtres')

# Filtre par langue
selected_languages = st.sidebar.multiselect('Langue', df_movies['language'].unique())
filtered_movies = df_movies[df_movies['language'].isin(selected_languages)]

# Filtre par pays
selected_countries = st.sidebar.multiselect('Pays', df_movies['country'].unique())
filtered_movies = filtered_movies[filtered_movies['country'].isin(selected_countries)]


# Bouton pour afficher les films recommandés
if st.sidebar.button('Afficher les recommandations'):
    # Compter les occurrences de chaque film dans les données filtrées
    movie_counts = filtered_movies['title'].value_counts()

    # Trier les films par popularité décroissante et obtenir les 10 premiers
    top_movies = movie_counts.head(10)

    # Afficher les 10 films les plus populaires
    st.header('Films recommandés')
    st.write(top_movies.to_markdown(numalign="left", stralign="left"))
