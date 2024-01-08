import plotly.express as px
import pandas as pd
import streamlit as st
import plotly
from filterData import netflix_data

static_country = ['Taiwan', 'Taiwan', 'Taiwan']
static_sales = [500, 200, 650]
static_sales = [i + 1 for i in range(len(static_sales))]
static_dates = ['2023-01-01', '2023-01-02', '2023-01-03']
print(netflix_data().head(3))

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
plotly.offline.plot(fig, filename="hold.html")