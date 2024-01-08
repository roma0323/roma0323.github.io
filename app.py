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

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
# # SAMPLE_SPREADSHEET_ID = ""
# SAMPLE_RANGE_NAME = "TV_Shows"
# SAMPLE_RANGE_NAME = ""


app = Flask(__name__)

@app.route("/")
def main():
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
    return render_template('vedioStyle/vedioStyle.html')

# 廖老大
@app.route("/rating")
def rating():
    return render_template('vedioRating/vedioRating.html')

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


