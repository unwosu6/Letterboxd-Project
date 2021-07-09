import requests
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import rotten_tomatoes_client
from rotten_tomatoes_client import RottenTomatoesClient
import csv
import plotly.express as px
import plotly.graph_objects as go
import time
from time import sleep
import os
import numpy as np

def user_input():
    user_name = input(
        ''' 
        Hello welcome to the letterboxd judger!
        To give a list of movies, download your rated movies from
        letterboxd.
        Upload the file within the zip file titled 'ratings.csv'.
        Thank you.
        Enter your letterboxd username below so we can add you 
        to our \"Movie Taste Database\": 
        ''')
    return user_name


def user_ratings_to_df(filename):
    try:
        ratings_df = pd.read_csv(filename)
        ratings_df.drop(['Date', 'Letterboxd URI'], axis=1, inplace=True)
        ratings_df.loc[ratings_df['Name'] == ratings_df.iloc[0]['Name'], 'Meter_Score'] = None
        ratings_df.loc[ratings_df['Name'] == ratings_df.iloc[0]['Name'], 'Difference'] = None
        ratings_df.loc[ratings_df['Name'] == ratings_df.iloc[0]['Name'], 'Actual_Difference'] = None        
    except File.DoesNotExist:
        print("The ratings.csv file was not provided. Goodbye.")
        exit()
    return ratings_df


def user_and_critic_df(ratings_df):
    numtry = 0
    for name, year, rating, meterScore, diff, acDiff in ratings_df.itertuples(index=False): 
        if numtry % 10 == 0:
            print("loading movies...")
        numtry += 1
        results = RottenTomatoesClient.search(term=name, limit=5)
        for result in results['movies']: 
            search_name = result['name']
            search_year = result['year']
            if (search_year == year 
                    or search_year == year + 1 
                    or search_year == year - 1) and search_name == name:
                if 'meterScore' in result.keys():
                    tomato = result['meterScore'] / 20.0
                    diff = rating - tomato
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Meter_Score'] = tomato
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Difference'] = abs(diff)
                    ratings_df.loc[  
                        ratings_df['Name'] == result['name'], 'Actual_Difference'] = diff
                else:
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Meter_Score'] = None
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Difference'] = None
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Actual_Difference'] = None
                break

    print('done loading movies!')
    ratings_df = ratings_df.astype({"Name":'string',
                    "Year":'float',
                    "Rating":'float',
                    "Meter_Score":'float',
                    "Difference":'float',
                    "Actual_Difference":'float'})
    
def plot_movie_ratings(username, ratings_df):
    fig = px.scatter(ratings_df, x='Rating', y='Meter_Score', hover_name='Name', color='Difference', 
                    labels={
                        'Rating': 'Your Rating',
                        'Meter_Score': 'Critic Rating',
                        'Difference': 'Difference in Ratings'
                     },
                    title = "Your Rating vs Critics Ratings")
    filename = username + '-ratings.html'
    file = fig.write_html(filename)


def save_database(database_name):
    os.system("mysqldump -u root -pcodio " + database_name + " > " + database_name + ".sql")


def load_database(database_name):
    os.system("mysql -u root -pcodio " + database_name + " < " + database_name + ".sql")

    
def user_data_to_database(database_name, user_name, ratings_df):
    load_database(database_name)
    engine = create_engine('mysql://root:codio@localhost/' + database_name) # add avg field
    ratings_df.to_sql(user_name, con=engine, if_exists='replace', index=False)
    ratings_df = ratings_df.dropna()
    if ratings_df.size == 0:
        sql = "REPLACE INTO letterboxd.all_users (username, average_difference) VALUES (\"" + user_name + "\", NULL);"
    else:
        avg = ratings_df['Difference'].mean()
        sql = "REPLACE INTO letterboxd.all_users (username, average_difference) VALUES (\"" + user_name + "\", " + str(avg) + ");"
    with engine.begin() as conn:
        conn.execute(sql)
    save_database(database_name)

    
def organize_ratings_df(ratings_df):
    ratings_df = ratings_df.dropna()
    if ratings_df.size == 0:
        avg = diff = movie_name = None
    else:
        # sort movies by difference in score
        ratings_df = ratings_df.sort_values(['Difference'], ascending=False)
        # average difference
        avg = ratings_df['Difference'].mean()
        # most differently rated movie
        movie_name = ratings_df.iloc[0]['Name']
        ac_diff = ratings_df.iloc[0]['Actual_Difference']
    return ratings_df, avg, movie_name, ac_diff


def get_controversial_scores(ratings_df):
    loved_movie = hated_movie = neutral_movie = None
    num_movies = ratings_df.index.size
    # find more specific data on likes and dislikes
    for i in range(1, num_movies):
        if ratings_df.iloc[i]['Actual_Difference'] > 0:
            loved_movie = ratings_df.iloc[i]['Name']
            break
    for i in range(1, num_movies):
        if ratings_df.iloc[i]['Actual_Difference'] < 0:
            hated_movie = ratings_df.iloc[i]['Name']
            break
    for i in reversed(range(1, num_movies)):
        if ratings_df.iloc[i]['Actual_Difference'] == 0:
            neutral_movie = ratings_df.iloc[i]['Name']
            break
    return hated_movie, loved_movie, neutral_movie


def user_output(ratings_df):
    ratings_df, avg, movie_name, ac_diff = organize_ratings_df(ratings_df)
    hated_movie, loved_movie, neutral_movie = get_controversial_scores(ratings_df)
    output = False
    if hated_movie != None:
        print('Wow, you think you\'re better than everyone for not liking %s?!' % (hated_movie))
        output = True
    if loved_movie != None:
        print('Whoa, seems like you liked %s a little too much...' % (loved_movie))
        output = True
    if neutral_movie != None:
        print('You can\'t even think for yourself! You rated %s the same as the critics.' % (neutral_movie))
        output = True
    if ac_diff != None:
        if ac_diff < 0:
            print('You had a %.2f difference with the critics on %s... You hated it but who\'s wrong here you (one person) or the critics (more than one person).' % (abs(ac_diff), movie_name))
        else:
            print('You had a %.2f difference with the critics on %s... You loved it but who\'s wrong here you (one person) or the critics (more than one person).' % (abs(diff), movie_name))
        if avg < 1:
            print('On average your rating was %.2f points different. You\'re an absolute sheep. No wonder people don\'t like your taste!' % (avg))
        else:
            print('On average your rating was %.2f points different. You\'re an absolute contrarian. No wonder people don\'t like your taste!' % (avg))
        output = True
    if output == False:
        print('Sorry you did not give us enough data... Goodbye.')