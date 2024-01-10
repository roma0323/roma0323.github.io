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

SAMPLE_RANGE_NAME = "TV_Shows"
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
    sheet = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME) 

    netflix_average_rate,hulu_average_rate,disney_average_rate,prime_vedio_average_rate = write_in_js(sheet)
    return render_template('vedioRating/vedioRating.html',Netflix_IMDb_rate=netflix_average_rate,
                           Hulu_IMDb_rate=hulu_average_rate,
                           Prime_IMDb_rate=disney_average_rate,
                           Disney_IMDb_rate=prime_vedio_average_rate)

def write_in_js(sheet):
     # filtered_data = sheet[sheet['IMDb']!= '']
    netflix_filtered_data = sheet[(sheet["Netflix"] == '1') & (sheet['IMDb']!= '')]
    hulu_filtered_data = sheet[(sheet["Hulu"] == '1') & (sheet['IMDb']!= '')]
    disney_filtered_data = sheet[(sheet["Prime Video"] == '1') & (sheet['IMDb']!= '')]
    prime_vedio_filtered_data = sheet[(sheet["Disney+"] == '1') & (sheet['IMDb']!= '')]
    # Extract the values from the "IMDb" column that satisfy the conditions

    netflix_imdb_list = netflix_filtered_data['IMDb'].tolist()
    netflix_number_list = [float(num) for num in netflix_imdb_list]
    netflix_average_rate = round(sum(netflix_number_list) / len(netflix_number_list),2)
    hulu_imdb_list = hulu_filtered_data['IMDb'].tolist()
    hulu_number_list = [float(num) for num in hulu_imdb_list]
    hulu_average_rate = round(sum(hulu_number_list) / len(hulu_number_list),2)
    disney_imdb_list = disney_filtered_data['IMDb'].tolist()
    disney_number_list = [float(num) for num in disney_imdb_list]
    disney_average_rate = round(sum(disney_number_list) / len(disney_number_list),2)
    prime_vedio_imdb_list = prime_vedio_filtered_data['IMDb'].tolist()
    prime_vedio_number_list = [float(num) for num in prime_vedio_imdb_list]
    prime_vedio_average_rate = round(sum(prime_vedio_number_list) / len(prime_vedio_number_list),2)

    import json

    # Convert the Python list to JSON string
    netflix_json_data = json.dumps(netflix_imdb_list)
    hulu_json_data = json.dumps(hulu_imdb_list)
    disney_json_data = json.dumps(disney_number_list)
    prime_vedio_json_data = json.dumps(prime_vedio_imdb_list)

 
        # Writing JSON data to a file
    with open('./static/assets/js/data.js', 'w') as js_file:
        js_file.write('\n')
        js_file.write(f'const Netflix_list = ')
        js_file.write(netflix_json_data)
        js_file.write(';')
        js_file.write('\n')
        js_file.write(f'const Hulu_list = ')
        js_file.write(hulu_json_data)
        js_file.write(';')
        js_file.write('\n')
        js_file.write(f'const Disney_list = ')
        js_file.write(disney_json_data)
        js_file.write(';')
        js_file.write('\n')
        js_file.write(f'const prime_video_list = ')
        js_file.write(prime_vedio_json_data)
        js_file.write(';')
        print(netflix_json_data)
        print("writinggggg")

    return netflix_average_rate,hulu_average_rate,disney_average_rate,prime_vedio_average_rate 

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
        platformData=["Netflix","Hulu","Prime Video","Disney+"]
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
            #print(temp.iloc[0])
            

            
    except HttpError as err:
        print(err)
    row, col = temp.shape
    return render_template('forms/recommondation.html',val=(temp.iloc[random.randint(0,row)]['Title']))
