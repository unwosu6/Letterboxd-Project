
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