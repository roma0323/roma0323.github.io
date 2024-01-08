from gsheet import get_sheet
from datetime import datetime
import plotly.express as px
import pandas as pd
import streamlit as st
import plotly

def make_bar_chart_race():
    # netflix_date = get_OTT_data("1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY","netflix_titles")   #get netflix date data
    # disney_plus_date = get_OTT_data("1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY","disney_plus_titles")   #get disney_plus date data
    # hulu_date = get_OTT_data("1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY","hulu_titles")   #get hulu date data
    

    # hulu_OTT = ['hulu'] * len(hulu_date)
    # hulu_quantity = [1] * len(hulu_date)
    # hulu_quantity = [i* + 1 for i in range(len(hulu_quantity))]
    
    # # disney_plus_OTT = ['disney_plus'] * len(disney_plus_date)
    # # disney_plus_quantity = [1] * len(disney_plus_date)
    # # disney_plus_quantity = [i* + 1 for i in range(len(disney_plus_quantity))]

    # netflix_OTT = ['netflix'] * len(netflix_date)
    # netflix_quantity = [1] * len(netflix_date)
    # netflix_quantity = [i* + 1 for i in range(len(netflix_quantity))]
    

    # static_dates = hulu_date+netflix_date
    # static_OTT = hulu_OTT+netflix_OTT
    # static_quantity = hulu_quantity+netflix_quantity

    # # static_dates = hulu_date+disney_plus_date+netflix_date
    # # static_OTT = hulu_OTT+disney_plus_OTT+netflix_OTT
    # # static_quantity = hulu_quantity+disney_plus_quantity+netflix_quantity


  

    
    # # Create a DataFrame with static values
    # data = {
    #     'OTT': static_OTT,
    #     'quantity': static_quantity,
    #     'Date': pd.to_datetime(static_dates)
    # }
    # df = pd.DataFrame(data)

    # # Store each column in a seperate varibale.
    # OTT = df["OTT"]
    # quantity = df["quantity"]
    # date = df["Date"].dt.strftime("%Y-%m-%d")

    # color_map = {
    #     'netflix': 'red',
    #     'hulu': 'orange',
    # }

    # # Create Animated Bar Chart and store figure as fig
    # fig = px.bar(
    #     df,
    #     x=OTT,
    #     y=quantity,
    #     color=OTT,
    #     animation_frame=date,
    #     animation_group=OTT,
    #     range_y=[0, 4000],)

    # # Save Chart and export to HTML
    # plotly.offline.plot(fig, filename="hold3.html")
    return None

def get_OTT_data(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME):

    sheet_data = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    converted_dates = []

    for date in sheet_data['date_added']:
        if date:  # 检查是否为空字符串
            try:
                dt = datetime.strptime(date, '%d-%b-%y')
                new_date = dt.replace(day=1)
                new_format = new_date.strftime('%Y-%m-%d')
                converted_dates.append(new_format)
            except ValueError:
                try:
                    # If the original format fails, try parsing with a different format
                    dt = datetime.strptime(date, '%B %d, %Y')
                    new_date = dt.replace(month=1,day=1)
                    new_format = new_date.strftime('%Y-%m-%d')
                    converted_dates.append(new_format)
                except ValueError:
                    print(f"Ignoring invalid date format: {date}")
                    continue
        else:
            print("Encountered an empty date string.")
            

    return converted_dates

