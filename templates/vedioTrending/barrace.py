# import plotly.express as px
# import pandas as pd
# import streamlit as st
# import plotly

# # Read Data From Excel and store in a variable df [dataframe]
# df = pd.read_excel("data.xlsx", usecols="A:C")
# print(df)
# df.dropna(inplace=True)

# # Store each column in a seperate varibale.
# df["Sales"]=1
# print(df["Sales"])
# country = df["Country"]
# sales = df["Sales"]
# date = df["Date"].dt.strftime("%Y-%m-%d")

# # Create Animated Bar Chart and store figure as fig
# fig = px.bar(
#     df,
#     x=country,
#     y=sales,
#     color=country,
#     animation_frame=date,
#     animation_group=country,
#     range_y=[0, 1200],
# )

# # Save Chart and export to HTML
# # plotly.offline.plot(fig, filename="Barrace.html")
# plotly.offline.plot(fig, filename="hold.html")
