import requests
import sqlalchemy
import pandas as pd
import rotten_tomatoes_client
from rotten_tomatoes_client import RottenTomatoesClient
import csv

def user_ratings_to_df(filename):
    # col_names = ['name', 'year', 'rating']
    # ratings_df = pd.DataFrame(col_names)
    ratings_df = pd.read_csv(lbxd_ratings)
    return ratings_df
    
# get the user's letterboxd ratings from their ratings.csv file
lbxd_ratings = "ratings.csv" # might want to use input function here
ratings_df = user_ratings_to_df(lbxd_ratings)

result = RottenTomatoesClient.search(term="Straight Up", limit=1)
print(result) # does not work for specific movies?
# match year and name string exactly
# what if there is no score?

#for movie in ratings_df['Name']:
#    result = RottenTomatoesClient.search(term=movie, limit=1)
#    print("tomatometer: %-10d" % (result['movies'][0]['meterScore']))
    # print("user score: %-10s --- tomatometer: %-10s" % (result['movies'][0]['name'] , result['movies'][0]['meterScore']))
