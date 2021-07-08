import letterboxd
from rotten_tomatoes_client import RottenTomatoesClient
import os

# create and save database to store multiple user's data
database_name = 'letterboxd'
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' + database_name + '; "')
letterboxd.save_database(database_name)

# get the user's letterboxd ratings from their ratings.csv file
lbxd_ratings = 'ratings.csv'  # might want to use input function here
user_name = letterboxd.user_input()
ratings_df = letterboxd.user_ratings_to_df(lbxd_ratings)
letterboxd.user_and_critic_df(ratings_df)
letterboxd.user_data_to_database(database_name, user_name, ratings_df)
letterboxd.plot_movie_ratings(ratings_df)

# results = RottenTomatoesClient.search(term='Portrait of a Lady on Fire', limit=5)
print(ratings_df)

# print(ratings_df.loc[ratings_df['Meter_Score'] == None, 'Name'])