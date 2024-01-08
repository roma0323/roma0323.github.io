from gsheet import get_sheet
from datetime import datetime
import plotly.express as px
import pandas as pd
import streamlit as st
import plotly

def netflix_data():
    SAMPLE_SPREADSHEET_ID = "1kd8gloSg7VE0aXvaSzBOqVDAX3nKfRXsoQBLZz_i1zY"
    SAMPLE_RANGE_NAME = "netflix_titles"
    sheet_data = get_sheet(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME)
    print(f"Spreadsheet: \n{sheet_data['date_added'].head()}")

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
                    new_date = dt.replace(day=1)
                    new_format = new_date.strftime('%Y-%m-%d')
                    converted_dates.append(new_format)
                except ValueError:
                    print(f"Ignoring invalid date format: {date}")
                    continue
        else:
            print("Encountered an empty date string.")
            
    print(f"Spreadsheet_date: \n{converted_dates[:20]}")




    static_dates = converted_dates
    static_country = ['netflix'] * len(static_dates)
    static_sales = [1] * len(static_dates)
    static_sales = [i*0.1 + 1 for i in range(len(static_sales))]
    
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
        range_y=[0, 1200],
    )

    # Save Chart and export to HTML
    plotly.offline.plot(fig, filename="hold3.html")


    return converted_dates


