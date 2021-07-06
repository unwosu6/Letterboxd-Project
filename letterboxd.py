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
    ratings_df.drop(['Date', 'Letterboxd URI'], axis=1, inplace=True)
    return ratings_df


# get the user's letterboxd ratings from their ratings.csv file
lbxd_ratings = "smaller.csv"  # might want to use input function here
ratings_df = user_ratings_to_df(lbxd_ratings)

# result = RottenTomatoesClient.search(term="Straight Up", limit=10)
# print(result) # does not work for specific movies?

# match year and name string exactly
# what if there is no score?

# results = RottenTomatoesClient.search(term='Hereditary', limit=5)
# print(results)

for name, year, rating in ratings_df.itertuples(index=False):
    results = RottenTomatoesClient.search(term=name, limit=5)
    for result in results['movies']:
        search_name = result['name']
        search_year = result['year']
        if search_year == year and search_name == name:
            if 'meterScore' in result.keys():
                print("user score: %-50s --- tomatometer: %-10d"
                      % (result['name'], result['meterScore']))
            else:
                print("user score: %-50s --- tomatometer: no score"
                      % (result['name']))
            break
