import letterboxd
from rotten_tomatoes_client import RottenTomatoesClient
import os

# create and save database to store multiple user's data
database_name = 'letterboxd'
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS ' + database_name + '; "')
os.system('mysql -u root -pcodio -e "CREATE TABLE IF NOT EXISTS letterboxd.all_users(username VARCHAR(255), average_difference FLOAT(3,2)); "')
letterboxd.save_database(database_name)

# get the user's letterboxd ratings from their ratings.csv file and the user's name
lbxd_ratings = 'ratings.csv'
user_name = letterboxd.user_input()

# create a dataframe for the user containing their movie ratings and the RT score
ratings_df = letterboxd.user_ratings_to_df(lbxd_ratings)
letterboxd.user_and_critic_df(ratings_df)

# outputs users results
# letterboxd.user_output(ratings_df)

# get the average difference and put the user's info into the database
letterboxd.user_data_to_database(database_name, user_name, ratings_df)

# provide user with visualization of movie taste
letterboxd.plot_movie_ratings(ratings_df)


# REMOVE 
# results = RottenTomatoesClient.search(term='Portrait of a Lady on Fire', limit=5)
print(ratings_df)

# print(ratings_df.loc[ratings_df['Meter_Score'] == None, 'Name'])