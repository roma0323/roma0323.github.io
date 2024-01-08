from gsheet import get_sheet
from datetime import datetime
import plotly.express as px
import pandas as pd
import streamlit as st
import plotly

def make_bar_chart_race():
    netflix_date = get_OTT_data("1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY","netflix_titles")   #get netflix date data
    disney_plus_date = get_OTT_data("1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY","disney_plus_titles")   #get disney_plus date data
    hulu_date = get_OTT_data("1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY","hulu_titles")   #get hulu date data
    

    hulu_country = ['hulu'] * len(hulu_date)
    hulu_sales = [1] * len(hulu_date)
    hulu_sales = [i* + 1 for i in range(len(hulu_sales))]
    
    # disney_plus_country = ['disney_plus'] * len(disney_plus_date)
    # disney_plus_sales = [1] * len(disney_plus_date)
    # disney_plus_sales = [i* + 1 for i in range(len(disney_plus_sales))]

    netflix_country = ['netflix'] * len(netflix_date)
    netflix_sales = [1] * len(netflix_date)
    netflix_sales = [i* + 1 for i in range(len(netflix_sales))]
    

    static_dates = hulu_date+netflix_date
    static_country = hulu_country+netflix_country
    static_sales = hulu_sales+netflix_sales

    # static_dates = hulu_date+disney_plus_date+netflix_date
    # static_country = hulu_country+disney_plus_country+netflix_country
    # static_sales = hulu_sales+disney_plus_sales+netflix_sales


  

    
    # Create a DataFrame with static values
    data = {
        'Country': static_country,
        'Sales': static_sales,
        'Date': pd.to_datetime(static_dates)
    }
    df = pd.DataFrame(data)

    # Store each column in a seperate varibale.
    country = df["Country"]
    sales = df["Sales"]
    date = df["Date"].dt.strftime("%Y-%m-%d")

    # Create Animated Bar Chart and store figure as fig
    fig = px.bar(
        df,
        x=country,
        y=sales,
        color=country,
        animation_frame=date,
        animation_group=country,
        range_y=[0, 6000],
    )

    # Save Chart and export to HTML
    plotly.offline.plot(fig, filename="hold3.html")


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

