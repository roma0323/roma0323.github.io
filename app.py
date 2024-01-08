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
from filterData.trendingData import netflix_data
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
    netflix_data()
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


# def get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME):
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """

#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=3000)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("sheets", "v4", credentials=creds)

#         # Call the Sheets API
#         sheet = service.spreadsheets()
#         result = (
#             sheet.values()
#             .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
#             .execute()
#         )
#         values = result.get("values", [])
#         if not values:
#             print("No data found.")
#         else:
#             print("Data found.")
#             df = pd.DataFrame(values)
#             # Get the first row for the header
#             df.columns = df.iloc[0]
#             # Take the data less the header row
#             df = df[1:]
#             # print the numbrr of rows
#             print(df.head())
            


#     except HttpError as err:
#         print(err)

#     return df
