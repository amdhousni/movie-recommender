import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Drop duplicates ##############################################################

def drop_duplicates(data, column, *, keep_start=None, keep_stop=None, break_at_first=False, ignore_index=False):

  # Columns to parse
  if type(keep_start) == int and type(keep_stop) == int:
    keep_cols = data.columns[keep_start:keep_stop]
  elif type(keep_start) == int:
    keep_cols = data.columns[keep_start:]
  elif type(keep_stop) == int:
    keep_cols = data.columns[:keep_stop]
  else:
    keep_cols = data.columns
  keep_cols = [c for c in keep_cols if c != column]

  # Duplicated rows: update the first duplicated row and delete the others
  duplicated = data[data[column].duplicated(keep=False) == True].sort_values(by=column)

  # Drop duplicates while keeping information
  index_first = None
  for index in duplicated.index:
    if index_first == None or data.loc[index, column] != data.loc[index_first, column]:
      index_first = index
    else:
      for c in keep_cols:
        if not pd.isna(data.loc[index, c]) and data.loc[index, c] and data.loc[index, c] != data.loc[index_first, c]:
          data.loc[index_first, c] = data.loc[index, c]
          if break_at_first: break
      data.drop(index=index, inplace=True)

  return data.reset_index(drop=True) if ignore_index else data


# ML - File creation for streamlit #############################################

def get_mlfile():
  ml_professionals = pd.read_csv(local_directory + "ml_professionals.csv")
  ml_movies = pd.read_csv(local_directory + "ml_movies.csv")

  # Use 'get_dummies' for 'genres' column
  ml_movies = pd.concat([ml_movies, ml_movies['genres'].str.get_dummies(sep=',').add(1)], axis=1)

  # Merge 'ml_movies' with 'ml_professionals' and fill NaN values with 0 for the 'ml_professionals' columns
  ml_movies = ml_movies.merge(ml_professionals, how='left', on='movieID').fillna(0)

  # Drop duplicates
  return drop_duplicates(ml_movies, 'movieID', keep_start=13, break_at_first=True, ignore_index=True)


# ML - Instantiate and fit the model ###########################################

def get_model(data, n_neighbors=10):

  # Define features
  X = data.select_dtypes(include='number')
  X = X[[c for c in X.columns if c not in ('runtime','budget','revenue','rentability','popularity','numVotes')]]

  # Standardize features by removing the mean and scaling to unit variance
  X_scaled = pd.DataFrame(StandardScaler().fit_transform(X), index=X.index, columns=X.columns)

  # Instantiate and fit the model
  model = NearestNeighbors(n_neighbors=n_neighbors).fit(X_scaled)

  return X_scaled, model


# ML - Get recommendations (nearest neighbors) #################################

def get_recommendations(model, data, X_scaled, target_column, neighbors_of, ncols=0):

  # Retrieve target data for recommendation
  _type = type(neighbors_of)
  df_neighbors_of = X_scaled[X_scaled.index.isin(data.loc[data[target_column].isin(neighbors_of.keys() if _type == dict else neighbors_of)].index)]

  # If more than one input, take the mean or the weighted mean
  if len(df_neighbors_of) > 1:
    if _type == dict:
      # Weighted mean
      first = True
      n_weights = 0
      for title, weight in neighbors_of.items():
        # Calculate the mean for duplicate titles
        serie = X_scaled[X_scaled.index.isin(data.loc[data[target_column].isin([title])].index)].mean(axis=0)
        if first:
          first = False
          resulting = weight * serie
        else:
          resulting = resulting + weight * serie
        n_weights += weight
      if n_weights != 0: resulting = resulting.div(n_weights)
    else:
      # Mean
      resulting = df_neighbors_of.mean(axis=0)
    # Convert to DataFrame and transpose the result
    resulting = pd.DataFrame(resulting).T
  else:
    resulting = df_neighbors_of

  # Retrieve the nearest neighbors
  nearest = model.kneighbors(resulting)

  # Select first 'ncols' columns if necessary and retrieve neighbors from their index
  _data = data[[column for i, column in enumerate(data.columns) if i < ncols]] if ncols > 0 else data
  recommendations = _data[data.index.isin(nearest[1][0])].copy().reset_index(drop=True)

  # Insert the 'distance' column
  recommendations.insert(2, 'distance', nearest[0][0].round(3))

  return recommendations

# Instantiate and fit the KNN model ############################################

if 'X_scaled' not in globals():
  # Get ML file
  top_movies = get_mlfile()

  # Number of neighbors required
  n_neighbors = 10
  # Target column for recommendation
  target_column = 'primaryTitle'
  # Proportion of the dataset to include in the train split

  # Instantiate and fit the KNN model
  X_scaled, distance = get_model(top_movies, n_neighbors=n_neighbors)


# Get recommendations: single input ############################################

get_recommendations(distance, top_movies, X_scaled, target_column, neighbors_of=['Forrest Gump'], ncols=12)

get_recommendations(distance, top_movies, X_scaled, target_column, neighbors_of=['Jurassic Park'], ncols=12)
# Get recommendations: more than one input #####################################
# Mean vector with a list

get_recommendations(distance, top_movies, X_scaled, 'primaryTitle', neighbors_of=['Mrs. Doubtfire','The Passion of the Christ'], ncols=12)
get_recommendations(distance, top_movies, X_scaled, target_column, neighbors_of=['Jurassic Park', 'Bridget Jones: The Edge of Reason'], ncols=12)
# Get recommendations: more than one input #####################################
# Weighted mean vector with a dictionnary

get_recommendations(distance, top_movies, X_scaled, 'primaryTitle', neighbors_of={'Jurassic Park':1, 'Bridget Jones: The Edge of Reason':10}, ncols=12)
