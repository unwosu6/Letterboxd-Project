import requests
import sqlalchemy
import pandas as pd
import rotten_tomatoes_client
from rotten_tomatoes_client import RottenTomatoesClient
import csv
import plotly.express as px
import plotly.graph_objects as go

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


def user_and_critic_df(ratings_df):
    for name, year, rating in ratings_df.itertuples(index=False):
        results = RottenTomatoesClient.search(term=name, limit=5)
        for result in results['movies']:
            search_name = result['name']
            search_year = result['year']
            if (search_year == year 
                or search_year == year + 1 
                or search_year == year - 1) and search_name == name:
                if 'meterScore' in result.keys():
                    tomato = result['meterScore'] / 20.0
                    diff = abs(tomato - rating)
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Meter_Score'] = tomato
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Difference'] = diff
                else:
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Meter_Score'] = None
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Difference'] = None
                break


def plot_movie_ratings(ratings_df):
    fig = px.scatter(ratings_df, x='Rating', y='Meter_Score', hover_name='Name', color='Difference')
    fig.write_html('ratings.html')


# get the user's letterboxd ratings from their ratings.csv file
lbxd_ratings = 'ratings.csv'  # might want to use input function here
ratings_df = user_ratings_to_df(lbxd_ratings)
user_and_critic_df(ratings_df)
plot_movie_ratings(ratings_df)

# issues: data takes time, maybe load in five at a time?
# issues/future: How to incorprate the use of databases in this
# future: output info to user abt what scores had biggest differences
# future: have the user input the file name
# future: put in try except blocks for possible errors (wrong file)
# future: right now we ignore movies we can't find on rt.
# future: expand to different review websites to find movies we can't initially find
# future: expand to other websites to get info on genre and studio

# results = RottenTomatoesClient.search(term='Straight Up', limit=5) cannot match year
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
