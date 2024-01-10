from flask import Flask, render_template
import os.path
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from filterData.trendingData import make_bar_chart_race
from filterData.trendingData import get_quantity_by_year
from gsheet import get_sheet
import filterData.styleData as styleData
import random


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
# SAMPLE_SPREADSHEET_ID = ""
SAMPLE_RANGE_NAME = "TV_Shows"
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
    return render_template('index.html')

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


# 睿弘
@app.route("/trending")
def trending():
    hulu_date_list,hulu_number_list=get_quantity_by_year("hulu_titles")
    netflix_date_list,netflix_number_list=get_quantity_by_year("netflix_titles")
    return render_template('vedioTrending/vedioTrending.html',
                           hulu_date_list=hulu_date_list,
                           hulu_number_list=hulu_number_list,
                           netflix_date_list=netflix_date_list,
                           netflix_number_list=netflix_number_list)


# 廖老大
@app.route("/rating")
def rating():
    SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
    SAMPLE_RANGE_NAME = "TV_Shows"
    global sheet
    if sheet is None:
        sheet = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME) 

    
    return render_template('vedioRating/vedioRating.html',
                            Netflix_IMDb_rate = write_in_js(sheet,'Netflix'),
                            Hulu_IMDb_rate = write_in_js(sheet,'Hulu'),
                            Prime_IMDb_rate = write_in_js(sheet,'Prime Video'),
                            Disney_IMDb_rate = write_in_js(sheet,'Disney+'))

def write_in_js(sheet,OTT_platform):
     # filtered_data = sheet[sheet['IMDb']!= '']
    

    filtered_data = sheet[(sheet[OTT_platform] == '1') & (sheet['IMDb']!= '')]

    # Extract the values from the "IMDb" column that satisfy the conditions
    imdb_list = filtered_data['IMDb'].tolist()

    number_list = [float(num) for num in imdb_list]

    average_rate = round(sum(number_list) / len(number_list),2)
    print(f'{OTT_platform} vedio average IMDb rate is:', average_rate)


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

    return average_rate        

# 李安之

@app.route("/form")
def form():
    return render_template('forms/form.html')

@app.route("/perference")
def perference():
    return render_template('forms/perferForm.html')

@app.route("/addForm")
def addForm():
    return render_template('forms/addForm.html')

@app.route("/addAmazonForm")
def addAmazonForm():
    return render_template('forms/addAmazonForm.html')


# Test connect to google sheet
@app.route("/test")
def test():
    SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
    SAMPLE_RANGE_NAME = "TV_Shows"
    get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    return render_template('index.html')


# Test add data to google sheet
@app.route("/add", methods=['POST'])
def add():
    if request.method=='POST':
        form_data=request.form
        print(form_data)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials_for_update.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('Datavisualization')
        worksheet = sheet.get_worksheet(0)  # Change the index to your desired worksheet
        platformData=["Netflix","hulu","primeVideo","Disney"]
        platformDataToAdd=[0,0,0,0]
        for i in range (4):
            if platformData[i]==form_data['platform']:
                platformDataToAdd[i]=1
                break
        data_to_add = ["", form_data['filmName'],form_data['year'],form_data['age'],form_data['IMDB'],form_data['RottenTomatoes'],platformDataToAdd[0],platformDataToAdd[1],platformDataToAdd[2],platformDataToAdd[3]]
        worksheet.append_row(data_to_add)
        return render_template('index.html',confirm="上傳成功")
    return render_template('index.html')


@app.route("/perferGet",methods=['POST'])
def perferGet():
     
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    df = pd.DataFrame()
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=3000)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
        else:
            print("Data found.")
            df = pd.DataFrame(values)
            # Get the first row for the header
            df.columns = df.iloc[0]
            # Take the data less the header row
            df = df[1:]
            # print the numbrr of rows
        if request.method=='POST':
            form_data=request.form
            platformData=["Netflix","Hulu","Prime Video","Disney+"]
            ageData=["7+","16+","18+"]
            temp = df[
                (pd.to_numeric(df['IMDb'], errors='coerce') >= float(form_data['IMDB']))
            ]
            for i in range(4):
                if form_data['platform']==platformData[i]:
                    temp=temp[temp[platformData[i]]=='1']
            for i in range(3):
                if form_data['age']==ageData[0]:
                    temp=temp[temp['Age']==ageData[0]]
                elif form_data['age']==ageData[1]:
                    temp=temp[(temp['Age']==ageData[0])|(temp['Age']==ageData[1])]
            print(temp.iloc[0])
            

            
    except HttpError as err:
        print(err)
        
    return render_template('forms/recommondation.html',val=(temp.iloc[0]['Title']))
