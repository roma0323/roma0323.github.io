from flask import Flask, render_template
import os.path
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from filterData.trendingData import make_bar_chart_race
from gsheet import get_sheet
import filterData.styleData as styleData

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
# # SAMPLE_SPREADSHEET_ID = ""
# SAMPLE_RANGE_NAME = "TV_Shows"
# SAMPLE_RANGE_NAME = ""
sheet = None
df_netflix_titles = None

app = Flask(__name__)

def init():
    SAMPLE_RANGE_NAME = "netflix_titles"
    global df_netflix_titles
    if df_netflix_titles is None:
        df_netflix_titles = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
        SAMPLE_RANGE_NAME = "disney_plus_titles"
        global df_disney_plus_titles
        df_disney_plus_titles = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
        SAMPLE_RANGE_NAME = "amazon_prime_titles"
        global df_amazon_prime_titles
        df_amazon_prime_titles = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
        SAMPLE_RANGE_NAME = "hulu_titles"
        global df_hulu_titles
        df_hulu_titles = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    return None


@app.route("/")
def main():
    init()
    fruits = ['apple', 'orange', 'pear', 'pineapple', 'durian']
    return render_template('index.html', fruits=fruits)

# 範例一
@app.route("/example1")
def example1():
    return render_template('publisherAnalysis.html')

# 範例二
@app.route("/example2")
def example2():
    return render_template('averageSales.html')

# 範例三
@app.route("/example3")
def example3():
    return render_template('barChartRace.html')

# Yasmine
@app.route("/style")
def style():
    listin_netflix_json, listin_disney_json, listin_amazon_json, listin_hulu_json = styleData.list_count()
    netflix_movie_tv_count_json, disney_movie_tv_count_json, amazon_movie_tv_count_json, hulu_movie_tv_count_json = styleData.movies_shows_count()
    season_count_json = styleData.one_season_count()

    return render_template('vedioStyle/vedioStyle.html', 
                           listin_netflix_json=listin_netflix_json, 
                           listin_disney_json=listin_disney_json, 
                           listin_amazon_json=listin_amazon_json, 
                           listin_hulu_json=listin_hulu_json, 
                           netflix_movie_tv_count_json=netflix_movie_tv_count_json, 
                           disney_movie_tv_count_json=disney_movie_tv_count_json, 
                           amazon_movie_tv_count_json=amazon_movie_tv_count_json, 
                           hulu_movie_tv_count_json=hulu_movie_tv_count_json,
                           season_count_json=season_count_json)

# 廖老大
@app.route("/rating")
def rating():
    SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
    SAMPLE_RANGE_NAME = "TV_Shows"
    global sheet
    if sheet is None:
        sheet = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME) 

    write_in_js(sheet,'Netflix')
    write_in_js(sheet,'Hulu')
    write_in_js(sheet,'Prime Video')
    write_in_js(sheet,'Disney+')
    
    return render_template('vedioRating/vedioRating.html')

def write_in_js(sheet,OTT_platform):
     # filtered_data = sheet[sheet['IMDb']!= '']
    

    filtered_data = sheet[(sheet[OTT_platform] == '1') & (sheet['IMDb']!= '')]

    # Extract the values from the "IMDb" column that satisfy the conditions
    imdb_list = filtered_data['IMDb'].tolist()

    import json

    # Convert the Python list to JSON string
    json_data = json.dumps(imdb_list)
    variable_exists = False

    if OTT_platform=='Prime Video':
        OTT_platform='prime_video'
    if OTT_platform=='Disney+':
        OTT_platform='Disney'    

    with open('./static/assets/js/data.js', 'r') as js_file:
        for line in js_file:
            if f'const {OTT_platform}_list =' in line:
                variable_exists = True
                break
                
    if not variable_exists:
        # Writing JSON data to a file
        with open('./static/assets/js/data.js', 'a') as js_file:
            js_file.write('\n')
            js_file.write(f'const {OTT_platform}_list = ')
            js_file.write(json_data)
            js_file.write(';')

# 睿弘
@app.route("/trending")
def trending():
    make_bar_chart_race()
    return render_template('vedioTrending/vedioTrending.html')

# Test connect to google sheet
@app.route("/test")
def test():
    SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
    SAMPLE_RANGE_NAME = "TV_Shows"
    get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    return render_template('index.html')


# Test add data to google sheet
@app.route("/add")
def add():
    # Define the scope and credentials JSON file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials_for_update.json', scope)

    # Authorize the credentials
    client = gspread.authorize(creds)

    # Open the desired Google Sheet by its title or URL
    sheet = client.open('Datavisualization')
    # Select the worksheet where you want to add data
    worksheet = sheet.get_worksheet(0)  # Change the index to your desired worksheet
    # Define the data you want to add in a list
    data_to_add = ["Value 1", "Value 2", "Value 3"]

    # Append the data to the worksheet
    worksheet.append_row(data_to_add)

    return render_template('index.html')


