import pandas as pd
import json
import app

def one_season_count():
    # count for netflix
    netflix_tiltes = app.df_netflix_titles
    netflix_one_season_count = netflix_tiltes[netflix_tiltes["duration"] == "1 Season"]["show_id"].count()
    disney_titles = app.df_disney_plus_titles
    disney_one_season_count = disney_titles[disney_titles["duration"] == "1 Season"]["show_id"].count()
    amazon_titles = app.df_amazon_prime_titles
    amazon_one_season_count = amazon_titles[amazon_titles["duration"] == "1 Season"]["show_id"].count()
    hulu_titles = app.df_hulu_titles
    hulu_one_season_count = hulu_titles[hulu_titles["duration"] == "1 Season"]["show_id"].count()
    df = pd.DataFrame({'platform': ['Netflix', 'Disney+', 'Amazon Prime', 'Hulu'], 'count': [netflix_one_season_count, disney_one_season_count, amazon_one_season_count, hulu_one_season_count]})
    # Convert the DataFrame to a dictionary in the desired format
    temp = df.set_index('platform')['count'].to_dict()
    # Convert the dictionary to JSON
    season_count_json = json.dumps(temp)
    return season_count_json


def movies_shows_count():
    netflix_tiltes = app.df_netflix_titles
    netflix_movie_count = netflix_tiltes[netflix_tiltes["type"] == "Movie"]["show_id"].count()
    netflix_tvshow_count = netflix_tiltes[netflix_tiltes["type"] == "TV Show"]["show_id"].count()
    df = pd.DataFrame({'type': ['Movie', 'TV Show'], 'count': [netflix_movie_count, netflix_tvshow_count]})
    # Convert the DataFrame to a dictionary in the desired format
    temp = df.set_index('type')['count'].to_dict()
    # Convert the dictionary to JSON
    netflix_movie_tv_count_json = json.dumps(temp)

    disney_titles = app.df_disney_plus_titles
    disney_movie_count = disney_titles[disney_titles["type"] == "Movie"]["show_id"].count()
    disney_tvshow_count = disney_titles[disney_titles["type"] == "TV Show"]["show_id"].count()
    df = pd.DataFrame({'type': ['Movie', 'TV Show'], 'count': [disney_movie_count, disney_tvshow_count]})
    # Convert the DataFrame to a dictionary in the desired format
    temp = df.set_index('type')['count'].to_dict()
    # Convert the dictionary to JSON
    disney_movie_tv_count_json = json.dumps(temp)

    amazon_titles = app.df_amazon_prime_titles
    amazon_movie_count = amazon_titles[amazon_titles["type"] == "Movie"]["show_id"].count()
    amazon_tvshow_count = amazon_titles[amazon_titles["type"] == "TV Show"]["show_id"].count()
    df = pd.DataFrame({'type': ['Movie', 'TV Show'], 'count': [amazon_movie_count, amazon_tvshow_count]})
    # Convert the DataFrame to a dictionary in the desired format
    temp = df.set_index('type')['count'].to_dict()
    # Convert the dictionary to JSON
    amazon_movie_tv_count_json = json.dumps(temp)

    hulu_titles = app.df_hulu_titles
    hulu_movie_count = hulu_titles[hulu_titles["type"] == "Movie"]["show_id"].count()
    hulu_tvshow_count = hulu_titles[hulu_titles["type"] == "TV Show"]["show_id"].count()
    df = pd.DataFrame({'type': ['Movie', 'TV Show'], 'count': [hulu_movie_count, hulu_tvshow_count]})
    # Convert the DataFrame to a dictionary in the desired format
    temp = df.set_index('type')['count'].to_dict()
    # Convert the dictionary to JSON
    hulu_movie_tv_count_json = json.dumps(temp)

    return netflix_movie_tv_count_json, disney_movie_tv_count_json, amazon_movie_tv_count_json, hulu_movie_tv_count_json

def list_count():
    # count for netflix
    listin_netflix = []
    for entry in app.df_netflix_titles['listed_in']:
        # Split the string on the comma
        split_strings = entry.split(',')
        # Strip leading and trailing spaces from each component
        cleaned_strings = [s.strip() for s in split_strings]
        # Add the cleaned strings to the gen list
        listin_netflix.extend(cleaned_strings)
    # turn gen into dataframe   
    listin_netflix=pd.DataFrame(listin_netflix,columns=['genre'])
    # count for netflix
    listin_netflix_count = listin_netflix.value_counts()
    # turn into json
    temp = listin_netflix_count.to_dict()
    temp1 = {','.join(map(str, k)): v for k, v in temp.items()}
    listin_netflix_json = json.dumps(temp1)

    # count for disney
    listin_disney = []
    for entry in app.df_disney_plus_titles['listed_in']:
        # Split the string on the comma
        split_strings = entry.split(',')
        # Strip leading and trailing spaces from each component
        cleaned_strings = [s.strip() for s in split_strings]
        # Add the cleaned strings to the gen list
        listin_disney.extend(cleaned_strings)
    # turn gen into dataframe   
    listin_disney=pd.DataFrame(listin_disney,columns=['genre'])
    # count for disney
    listin_disney_count = listin_disney.value_counts()
    # turn into json
    temp = listin_disney_count.to_dict()
    temp1 = {','.join(map(str, k)): v for k, v in temp.items()}
    listin_disney_json = json.dumps(temp1)

    # count for amazon
    listin_amazon = []
    for entry in app.df_amazon_prime_titles['listed_in']:
        # Split the string on the comma
        split_strings = entry.split(',')
        # Strip leading and trailing spaces from each component
        cleaned_strings = [s.strip() for s in split_strings]
        # Add the cleaned strings to the gen list
        listin_amazon.extend(cleaned_strings)
    # turn gen into dataframe   
    listin_amazon=pd.DataFrame(listin_amazon,columns=['genre'])
    # count for amazon
    listin_amazon_count = listin_amazon.value_counts()
    # turn into json
    temp = listin_amazon_count.to_dict()
    temp1 = {','.join(map(str, k)): v for k, v in temp.items()}
    listin_amazon_json = json.dumps(temp1)

    # count for hulu
    listin_hulu = []
    for entry in app.df_hulu_titles['listed_in']:
        # Split the string on the comma
        split_strings = entry.split(',')
        # Strip leading and trailing spaces from each component
        cleaned_strings = [s.strip() for s in split_strings]
        # Add the cleaned strings to the gen list
        listin_hulu.extend(cleaned_strings)
    # turn gen into dataframe   
    listin_hulu=pd.DataFrame(listin_hulu,columns=['genre'])
    # count for hulu
    listin_hulu_count = listin_hulu.value_counts()
    # turn into json
    temp = listin_hulu_count.to_dict()
    temp1 = {','.join(map(str, k)): v for k, v in temp.items()}
    listin_hulu_json = json.dumps(temp1)

    return listin_netflix_json, listin_disney_json, listin_amazon_json, listin_hulu_json