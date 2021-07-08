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
        ratings_df.loc[ratings_df['Name'] == ratings_df.iloc[0]['Name'], 'Meter_Score'] = None
        ratings_df.loc[ratings_df['Name'] == ratings_df.iloc[0]['Name'], 'Difference'] = None
        ratings_df.loc[ratings_df['Name'] == ratings_df.iloc[0]['Name'], 'Actual_Difference'] = None        
        #ratings_df = ratings_df.assign(Meter_Score='', Difference='', Actual_Difference='')
        #df.assign(ColName='') 
        #df = df.assign(Empty_Col1='', Empty_Col2='')
    except:
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
    print(ratings_df)
    ratings_df = ratings_df.astype({"Name":'string',
                    "Year":'float',
                    "Rating":'float',
                    "Meter_Score":'float',
                    "Difference":'float',
                    "Actual_Difference":'float'})

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
    # keeps adding same user on multiple runsexi
    sql = "INSERT INTO letterboxd.all_users (username, average_difference) VALUES (\"" + user_name + "\", " + str(avg) + ");"
    with engine.begin() as conn:
        conn.execute(sql)
    # ratings_df.to_sql("all_users", con=engine, if_exists='replace', index=False)
    # INSERT INTO catalog (name,manufacture_year,brand)
    # VALUES ("Brian May’s Red Special", 1963, DEFAULT);
    save_database(database_name)

    
def organize_ratings_df(ratings_df):
    # sort movies by difference in score
    ratings_df = ratings_df.sort_values(['Difference'], ascending=False)
    # average difference
    avg = ratings_df['Difference'].mean()
    # most differently rated movie
    movie_name = ratings_df.iloc[0]['Name']
    diff = ratings_df.iloc[0]['Actual_Difference']
    return ratings_df, avg, movie_name, diff

def get_controversial_scores(ratings_df):
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
        else:
            neutral_movie = None
    return hated_movie, loved_movie, neutral_movie
        
def user_output(ratings_df):
    ratings_df, avg, movie_name, diff = organize_ratings_df(ratings_df)
    hated_movie, loved_movie, neutral_movie = get_controversial_scores(ratings_df)
    print('Wow, you think you\'re better than everyone for not liking %s?!' % (hated_movie))
    print('Whoa, seems like you liked %s a little too much...' % (loved_movie))
    print('You can\'t even think for yourself! You rated %s the same as the critics.' % (neutral_movie))
    
    if diff < 0:
        print('You had a %.2f difference with the critics on %s... You loved it but who\'s wrong here you (one person) or the critics (more than one person).' % (abs(diff), movie_name))
    else:
        print('You had a %.2f difference with the critics on %s... You hated it but who\'s wrong here you (one person) or the critics (more than one person).' % (abs(diff), movie_name))
    
    if avg < 1:
        print('On average your rating was %.2f points different. You\'re an absolute sheep. No wonder people don\'t like you... r taste!' % (avg))
    else:
        print('On average your rating was %.2f points different. You\'re an absolute contrarian. No wonder people don\'t like you... r taste!' % (avg))


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

        