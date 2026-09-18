import pandas as pd
import requests
import json
import os

def extract_weather_data():

    csv_path = "/opt/airflow/dags/bronze/ma.csv"
    output_dir = "/opt/airflow/dags/bronze/weather"
    output_path = os.path.join(output_dir, "Weather.json")  

    os.makedirs(output_dir, exist_ok=True)

    cities = pd.read_csv(csv_path)

    weather_results = {}

    for index, row in cities.iterrows():

        city_name = row["city"]
        latitude = row["lat"]
        longitude = row["lng"]

        print(f"Fetching weather data for {city_name}...")

        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "daily": [
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                        "precipitation_probability_max",
                        "wind_speed_10m_max",
                        "wind_gusts_10m_max",
                        "weather_code"
                    ],
                    "forecast_days": 7,
                    "timezone": "auto"
                },
                timeout=10
            )

            response.raise_for_status()

            weather_data = response.json()

            weather_results[city_name] = {
                "latitude": latitude,
                "longitude": longitude,
                "weather": weather_data
            }

            print(f"Weather data for {city_name} collected.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data for {city_name}: {e}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response for {city_name}: {e}")
        

    with open(output_path, "w") as file:
        json.dump(weather_results, file,indent=4)

    print(f"\nAll weather data saved to {output_path}")

    
