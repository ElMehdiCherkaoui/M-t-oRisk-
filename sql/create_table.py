from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

try:
    engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5433/mydatabase')
except Exception as e:
    print("Error connecting to the database:", e)
    
SessionLocal = sessionmaker(autocommit=False, bind=engine) 
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

Base.metadata.create_all(bind=engine)

json_path = "gold/weather/Weather_final.json"
weather_df = pd.read_json(json_path)

session = SessionLocal()    

for index, row in weather_df.iterrows():
    weather_risk = WeatherRiskGold(
        city=row['city'],
        forecast_date=row['date'],
        latitude=row['latitude'],
        longitude=row['longitude'],
        temp_max=row['temp_max'],
        temp_min=row['temp_min'],
        wind_speed=row['wind_speed'],
        wind_gusts=row['wind_gusts'],
        precipitation=row['precipitation'],
        precipitation_probability=row['precipitation_probability'],
        temperature_category=row['temperature_category'],
        wind_category=row['wind_category'],
        rain_category=row['rain_category'],
        risk_score=row['risk_score'],

        
    )
    
    session.merge(weather_risk)

session.commit()
session.close()

print("Data inserted into the weather_risk_gold table successfully.")