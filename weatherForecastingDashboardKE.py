import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

#source: https://github.com/null-jones/streamlit-plotly-events
from streamlit_plotly_events import plotly_events

import numpy as np
import plotly.express as px


st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title='Weather Forecasting Dashboard KE')
#figure_show = selected_points = plotly_events(figure)

# Loading the available data and overview
path = ".../weatherDataSet.csv"
st.sidebar.header('Weather Forecasting KE')
st.sidebar.write('''This is a Weather Forecasting App, that uses historical data of Nairobi, Kenya. The data dates back 2023 to ...''')

# Overview of the data set
data = pd.read_csv(path)
st.header('Data set overview')
st.write(data.head())

# Descriptive statistics of the data
st.header('Descriptive statistics of the data')
st.write(data.describe())

# Looking at the information about all the columns in the dataset
st.header('Data columns descriptions')
st.write(data.info())

# Mean Temperature in Delhi over the years
st.header('Mean Temperature in Nairobi over the years')
figure = px.line(data, x="date",
		y="meantemp",
		title="Mean Temperature in Nairobi over the years")
selected_points = plotly_events(figure)
#figure_show

# Humidity
st.header('Humidity in Nairobi over the years')
figure = px.line(data, x="date",
		y="humidity",
		title='Humidity in Nairobi Over the Years')
selected_points = plotly_events(figure)
#figure_show

# Wind Speed
st.header('Wind Speed in Nairobi over the years')
figure = px.line(data, x="date",
		y="wind_speed",
		title='Wind Speed in Nairobi over the years')
selected_points = plotly_events(figure)
#figure_show
st.write('Till 2015, the wind speed was higher during monsoons(August & Septembder) and retreating monsoons(December & January). After 2015, there were no anomalies in wind speed during monsoons.')

# Relationship between Temperature and Humidity
st.header('Relationship between Temperature and Humidity')
figure = px.scatter(data_frame = data, x="humidity",
		y="meantemp", size="meantemp", trendline="ols",
		title="Relationship Between Temperature and Humidity.")
selected_points = plotly_events(figure)

# calculate correlation coefficient
correlation = data['humidity'].corr(data['meantemp'])
st.write("The correlation value is: " ,correlation)

st.write('There is a negative correlation between temperature and humidity in Nairobi. It means higher temperature results in low humidity and lower temperature results in high humidity.')

# Analyzing Temperature Change

# converting data type of the date column into datetime
st.header('date column into datetime format')
data["date"] = pd.to_datetime(data["date"], format = '%Y-%m-%d')
data["year"] = data["date"].dt.year
data["month"] = data["date"].dt.month
st.write(data.head())

# Temperature change in Delhi over the years
st.header('Temperature change in Nairobi over the years')
plt.style.use('fivethirtyeight')
plt.figure(figsize=(15, 10))
plt.title("Temperature Change in Nairobi Over the Years")
sns.lineplot(data = data, x='month', y='meantemp', hue='year')
st.pyplot()
st.write('Although 2017 was not the hottest year in the summer, we can see a rise in the average temperature of Nairobi every year')

# Forecasting Weather using Python
st.header('Forecasting Weather KE')
st.write('The Facebook prophet model will be used for this task')

st.subheader('Converting the data format')
st.write('The prophet model accepts data named as "ds", and labels as "y". Where "y": meantemp, and "ds": date ')
forecast_data = data.rename(columns = {"date": "ds",
"meantemp": "y"})
st.write(forecast_data)

# How the Facebook propher model can be used for weather forecasting
st.header('How the Facebook model can be used for Weather Forecasting using Python')



from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

model = Prophet()
model.fit(forecast_data)
forecasts = model.make_future_dataframe(periods=365)
predictions = model.predict(forecasts)
fig = plot_plotly(model, predictions)
st.plotly_chart(fig, theme=None, use_container_width=True)




