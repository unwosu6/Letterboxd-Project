import requests
import sqlalchemy
import pandas as pd
import rotten_tomatoes_client
from rotten_tomatoes_client import RottenTomatoesClient
import csv

def user_input():
    lbxd_ratings = input(
        ''' 
        Hello welcome to the letterboxd judger! \n
        To give a list of movies, download your rated movies from
        letterboxd. \n Upload the file within the zip file titled 
        'ratings.csv'. \n Thank you. \n
        ''')
    return lbxd_ratings


def user_ratings_to_df(filename):
    ratings_df = pd.read_csv(lbxd_ratings)
    ratings_df.drop(['Date', 'Letterboxd URI'], axis=1, inplace=True)
    return ratings_df


def user_and_audience_df(ratings_df):
    # meter_score_list = []
    for name, year, rating in ratings_df.itertuples(index=False):
        results = RottenTomatoesClient.search(term=name, limit=5)
        for result in results['movies']:
            search_name = result['name']
            search_year = result['year']
            if search_year == year and search_name == name:
                if 'meterScore' in result.keys():
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Meter_Score'] = (result['meterScore'] / 20.0)
                else:
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Meter_Score'] = None
                break
    print(ratings_df)

# get the user's letterboxd ratings from their ratings.csv file
lbxd_ratings = 'smaller.csv'  # might want to use input function here
ratings_df = user_ratings_to_df(lbxd_ratings)

user_and_audience_df(ratings_df) # needs to be fixed; add meterScore specific to movie name
#print(ratings_df)

# results = RottenTomatoesClient.search(term='Straight Up', limit=5) cannot match year !
# print(results)

# for name, year, rating in ratings_df.itertuples(index=False):
#     results = RottenTomatoesClient.search(term=name, limit=5)
#     for result in results['movies']:
#         search_name = result['name']
#         search_year = result['year']
#         if search_year == year and search_name == name:
#             if 'meterScore' in result.keys():
#                 print("movie name: %-50s user score: %1d --- tomatometer: %-10d"
#                       % (result['name'], rating, result['meterScore']))
#             else:
#                 print("movie name: %-50s user score: %1d --- tomatometer: no score"
#                       % (result['name'], rating))   
#             break
