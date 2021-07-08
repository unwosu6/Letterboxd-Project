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

def user_input():
    user_name = input(
        ''' 
        Hello welcome to the letterboxd judger!
        To give a list of movies, download your rated movies from
        letterboxd.
        Upload the file within the zip file titled 'ratings.csv'.
        Thank you.
        Enter your letterboxd username below so we can add you to our \"Movie Taste Database\": 
        ''')
    return user_name


def user_ratings_to_df(filename):
    try:
        ratings_df = pd.read_csv(filename)
        ratings_df.drop(['Date', 'Letterboxd URI'], axis=1, inplace=True)
    except:
        print("The ratings.csv file was not provided. Goodbye.")
        exit()
    return ratings_df


def user_and_critic_df(ratings_df):
#     length = len(ratings_df.index)
#     for i in range(length/5):
#         search_next_five(ratings_df)
    numtry = 0
    for name, year, rating in ratings_df.itertuples(index=False):
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
                    diff = abs(tomato - rating)
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Meter_Score'] = tomato
                    ratings_df.loc[
                        ratings_df['Name'] == result['name'], 'Difference'] = diff
                else:
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Meter_Score'] = None
                    ratings_df.loc[ratings_df['Name'] == result['name'], 'Difference'] = None
                break
        if numtry % 10 == 0:
            print("temp")
            # sleep(1)


def plot_movie_ratings(ratings_df):
    fig = px.scatter(ratings_df, x='Rating', y='Meter_Score', hover_name='Name', color='Difference')
    fig.write_html('ratings.html')


def save_database(database_name):
    os.system("mysqldump -u root -pcodio " + database_name + " > " + database_name + ".sql")


def load_database(database_name):
    os.system("mysql -u root -pcodio " + database_name + " < " + database_name + ".sql")


def user_data_to_database(database_name, user_name, ratings_df):
    load_database(database_name)
    engine = create_engine('mysql://root:codio@localhost/' + database_name) # add avg field
    ratings_df.to_sql(user_name, con=engine, if_exists='replace', index=False)
    avg = ratings_df['Difference'].mean()
    # think abt updating a master table with columns: user_name, avg difference
    print("here is the problem")
    sql = "INSERT INTO letterboxd.all_users (username, average_difference) VALUES (\"" + user_name + "\", " + str(avg) + ");"
    with engine.begin() as conn:
        conn.execute(sql)
    # ratings_df.to_sql("all_users", con=engine, if_exists='replace', index=False)
    # INSERT INTO catalog (name,manufacture_year,brand)
    # VALUES ("Brian May’s Red Special", 1963, DEFAULT);
    print("can't get here")
    save_database(database_name)


def user_output(ratings_df):
    #ratings_df = ratings_df.sort_values(['Difference'], axis=1, ascending=False)
    #print(ratings_df.head()) 
    pass

# issues: data takes time, maybe load in five at a time?
# issues/future: How to incorprate the use of databases in this
# future: output info to user abt what scores had biggest differences
# future: have the user input the file name
# future: put in try except blocks for possible errors (wrong file)
# future: right now we ignore movies we can't find on rt.
# future: expand to different review websites to find movies we can't initially find
# future: expand to other websites to get info on genre and studio
# flow diagram to explain what csv is for vs what api is for
# expansion: if you record for a differt user on average how different they are with their music taste
# after n number of users you can show that how each user compares to eachother with their difference
# on average
# bar graphs could be interestings to see how many things they rated
# axis could be the differences. are there lots of differences or are there lots of things different

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
