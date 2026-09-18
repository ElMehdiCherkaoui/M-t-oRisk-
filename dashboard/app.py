from sqlalchemy import Column, Date, Float, Integer, String, create_engine, func
from sqlalchemy.orm import sessionmaker ,declarative_base

import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px

DATABASE_URL = 'postgresql://postgres:postgres@meteorisK-db:5432/postgres'


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class WeatherRiskGold(Base):
    __tablename__ = 'weather_risk_gold'

    city = Column(String, primary_key=True)
    forecast_date = Column(Date, primary_key=True)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    temp_max = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_gusts = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=False)
    precipitation_probability = Column(Float, nullable=False)
    
    temperature_category = Column(String, nullable=False)
    wind_category = Column(String, nullable=False)
    rain_category = Column(String, nullable=False)

    
    
    
    risk_score = Column(Integer, nullable=False)
        

try:
    df = session.query(WeatherRiskGold).all()
    df = pd.DataFrame([{
        'city': row.city,
        'forecast_date': row.forecast_date,
        'latitude': row.latitude,
        'longitude': row.longitude,
        'temp_max': row.temp_max,
        'temp_min': row.temp_min,
        'wind_speed': row.wind_speed,
        'wind_gusts': row.wind_gusts,
        'precipitation': row.precipitation,
        'precipitation_probability': row.precipitation_probability,
        'temperature_category': row.temperature_category,
        'wind_category': row.wind_category,
        'rain_category': row.rain_category,
        'risk_score': row.risk_score
    } for row in df])
except Exception as e:
    print(f"Error occurred while fetching data: {e}")
finally:
    session.close()
    
    

st.sidebar.title("Weather Risk Dashboard")

all_cities = df['city'].unique()

min_date = df['forecast_date'].min()
max_date = df['forecast_date'].max()

selected_dates = st.sidebar.date_input(
    "Select Forecast Period", 
    value=(min_date, max_date), 
    min_value=min_date, 
    max_value=max_date
)

if len(selected_dates) == 2:
    start_date, end_date = (selected_dates[0], selected_dates[1])
else:
    start_date = end_date = selected_dates[0]
    


selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=all_cities,
    default=all_cities
)

selected_temperature = st.sidebar.multiselect(
    "Select Temperature Category",
    options=df['temperature_category'].unique(),
    default=df['temperature_category'].unique()
)

selected_wind = st.sidebar.multiselect(
    "Select Wind Category",
    options=df['wind_category'].unique(),
    default=df['wind_category'].unique()
)

selected_rain = st.sidebar.multiselect(
    "Select Rain Category",
    options=df['rain_category'].unique(),
    default=df['rain_category'].unique()
)

selected_risk_score = st.sidebar.slider(
    "Select Risk Score Range",
    min_value=int(df['risk_score'].min()),
    max_value=int(df['risk_score'].max()),
    value=(int(df['risk_score'].min()), int(df['risk_score'].max()))
)

df_filtered = df[
    (df['forecast_date'].between(start_date, end_date)) & 
    (df['city'].isin(selected_cities)) & 
    (df['temperature_category'].isin(selected_temperature)) & 
    (df['wind_category'].isin(selected_wind)) &
    (df['rain_category'].isin(selected_rain)) &
    (df['risk_score'].between(selected_risk_score[0], selected_risk_score[1]))
]

set_columns = st.columns(3)
with set_columns[0]:
    st.metric("Average Max Temp", round(df_filtered['temp_max'].mean(), 2))
with set_columns[1]:
    st.metric("Max rain", round(df_filtered['precipitation'].max(), 2))
with set_columns[2]:
    st.metric("total cities", df_filtered['city'].nunique())
    


st.subheader("Max Temperature by City")

city_max_temps = df_filtered.groupby('city')['temp_max'].max().reset_index()
city_max_temps = city_max_temps.sort_values(by='temp_max', ascending=False).head(10)
fig_temp, ax_temp = plt.subplots(figsize=(10, 5)) 
sns.barplot(
    data=city_max_temps, 
    x='city', 
    y='temp_max', 
    ax=ax_temp
)

ax_temp.set_title('Maximum Expected Temperature per City')
ax_temp.set_xlabel('City')
ax_temp.set_ylabel('Temperature (°C)')
plt.xticks(rotation=45)
st.pyplot(fig_temp)





st.subheader("Maximum Precipitation by City")

city_max_precipitation = df_filtered.groupby('city')['precipitation'].max().reset_index()
city_max_precipitation = city_max_precipitation.sort_values(by='precipitation', ascending=False).head(10)

fig_rain, ax_rain = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=city_max_precipitation, 
    x='city', 
    y='precipitation', 
    ax=ax_rain
)

ax_rain.set_title('Maximum Expected Precipitation per City')
ax_rain.set_xlabel('City')
ax_rain.set_ylabel('Precipitation (mm)')
plt.xticks(rotation=45)
st.pyplot(fig_rain)




st.subheader("Risk Score Timeline")

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(   
    data=df_filtered, 
    x='forecast_date', 
    y='risk_score',  
    hue='city',   
    marker='o',
    ax=ax
)

ax.set_title('Risk Score Forecast Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Risk Score (0-100)')
plt.xticks(rotation=45)
plt.legend().remove()
st.pyplot(fig)


st.subheader("cities with risk score >= 1")

danger_cities = df_filtered[df_filtered['risk_score'] >= 1]

if danger_cities.any():
    fig = px.scatter_mapbox(
        danger_cities,
        lat='latitude',
        lon='longitude',
        size='risk_score',
        color='risk_score',
        color_continuous_scale="Reds",
        hover_name='city',
        opacity=0.7,
        zoom=5,
        labels={'risk_score': 'Risk Score'},
    )

    fig.update_layout(
        mapbox_style="open-street-map",
    )

    st.plotly_chart(fig)
else:
    st.info("No cities match the risk criteria.")