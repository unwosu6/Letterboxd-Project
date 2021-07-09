import letterboxd
from rotten_tomatoes_client import RottenTomatoesClient
import os
import pandas as pd

# create and save database to store multiple user's data
database_name = 'letterboxd'
os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
          + database_name + '; "')
os.system('mysql -u root -pcodio -e "CREATE TABLE IF NOT EXISTS '
          + 'letterboxd.all_users(username VARCHAR(255), average_difference'
          + ' FLOAT(3,2), PRIMARY KEY (username)); "')
letterboxd.save_database(database_name)

# get the username and letterboxd ratings from their ratings.csv
lbxd_ratings = 'ratings1.csv'
username = letterboxd.user_input()

# check if the user is returning
response = input('Are providing new data? [Y/N]: ').lower()
filename = username + ".csv"
if response == 'n': 
    ratings_df = letterboxd.returning_user(username, database_name)
else:
    # create dataframe containing user movie ratings and the RT score
    ratings_df = letterboxd.user_ratings_to_df(lbxd_ratings)
    ratings_df = letterboxd.user_and_critic_df(ratings_df)

# outputs users results
letterboxd.user_output(ratings_df)
# get the average difference and put the user's info into the database
letterboxd.user_data_to_database(database_name, username, ratings_df)
# provide user with visualization of movie taste
letterboxd.plot_movie_ratings(username, ratings_df)
