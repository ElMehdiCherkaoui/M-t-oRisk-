import pandas as pd
import json
import os

json_path = "silver/weather/Weather_cleaned.json"
output_dir = "gold/weather"
output_path = os.path.join(output_dir, "Weather_final.json")

os.makedirs(output_dir, exist_ok=True)

weather_df = pd.read_json(json_path)



def categorize_temp(row):
    if row['temp_max'] > 45:
        return 'High Risk Heat'
    elif row['temp_min'] < 5:
        return 'Low Risk Cold'
    else:
        return 'Optimal'
    
def categorize_wind(row):
    if row['wind_speed'] > 40:
        return 'High Risk Wind'
    elif row['wind_gusts'] > 65:
        return 'High Risk Gusts'
    else:
        return 'Optimal'

def categorize_rain(row):
    if row['precipitation'] > 30:
        return 'High Risk Rain'
    elif row['precipitation_probability'] > 80:
        return 'High Risk Probability'
    else:
        return 'Optimal'
    
def calculate_risk(row):
    risk_score = 0
    if row['temperature_category'] == 'High Risk Heat':
        risk_score += 35
    elif row['temperature_category'] == 'Low Risk Cold':
        risk_score += 1

    if row['wind_category'] == 'High Risk Wind':
        risk_score += 35
    elif row['wind_category'] == 'High Risk Gusts':
        risk_score += 1

    if row['rain_category'] == 'High Risk Rain':
        risk_score += 30
    elif row['rain_category'] == 'High Risk Probability':
        risk_score += 1

    return risk_score


    
    


weather_df['temperature_category'] = weather_df.apply(categorize_temp, axis=1)
weather_df['wind_category'] = weather_df.apply(categorize_wind, axis=1)
weather_df['rain_category'] = weather_df.apply(categorize_rain, axis=1)
weather_df['risk_score'] = weather_df.apply(calculate_risk, axis=1)

weather_df.to_json(output_path, orient='records', date_format='iso', indent=4)
