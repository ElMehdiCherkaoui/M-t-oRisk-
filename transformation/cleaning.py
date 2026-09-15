import pandas as pd
import json
import os

json_path = "bronze/weather/Weather.json"
cities_path = "bronze/ma.csv"

output_dir = "silver/weather"
output_path = os.path.join(output_dir, "Weather_cleaned.json")

os.makedirs(output_dir, exist_ok=True)

weather_results = []


with open(json_path, "r") as file:
    cities_weather = json.load(file)


for city_name, data in cities_weather.items():

    latitude = data["latitude"]
    longitude = data["longitude"]

    daily_weather = data["weather"]["daily"]

    dates = daily_weather["time"]
    temperatures_max = daily_weather["temperature_2m_max"]
    temperatures_min = daily_weather["temperature_2m_min"]
    precipitation = daily_weather["precipitation_sum"]
    precipitation_probability = daily_weather["precipitation_probability_max"]
    wind_speed = daily_weather["wind_speed_10m_max"]
    wind_gusts = daily_weather["wind_gusts_10m_max"]
    weather_codes = daily_weather["weather_code"]

    for i in range(len(dates)):
        weather_results.append({
            "city": city_name,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "date": dates[i],
            "temp_max": float(temperatures_max[i]),
            "temp_min": float(temperatures_min[i]),
            "precipitation": float(precipitation[i]),
            "precipitation_probability": int(precipitation_probability[i]),
            "wind_speed": float(wind_speed[i]),
            "wind_gusts": float(wind_gusts[i]),
            "weather_code": int(weather_codes[i])
        })

df = pd.DataFrame(weather_results)

df["date"] = pd.to_datetime(df["date"])

df = df.drop_duplicates(subset=["city", "date"])

df = df[
    (df["temp_max"] >= df["temp_min"]) &
    (df["precipitation"] >= 0) &
    (df["precipitation_probability"].between(0, 100)) &
    (df["wind_speed"] >= 0) &
    (df["wind_gusts"] >= 0)
]

cities = pd.read_csv(cities_path)

cities = cities[
    [
        "city",
        "country",
        "iso2",
        "admin_name",
        "capital",
        "population",
        "population_proper"
    ]
]

df = df.merge(
    cities,
    on="city",
    how="left"
)

df.to_json(
    output_path,
    orient="records",
    date_format="iso",
    indent=4
)

print(f"\nSilver data saved to: {output_path}")
print("\nFirst 5 rows:")
print(df.head())