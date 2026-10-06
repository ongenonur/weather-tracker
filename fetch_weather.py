
# Imported existing modules. csv for handling read/write spreadsheets. datetime ofor getting computers current clock time,
# requests is a HTTP library
import csv
import datetime
import os
import requests

# Exact coordinates for Pisac, Sacred Valley, Peru
LATITUDE = -13.4214898
LONGITUDE = -71.8399634
CSV_FILE = "pisac_weather_log.csv"

import os
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

# Read API keys safely from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "")
TOMORROW_API_KEY = os.getenv("TOMORROW_API_KEY", "")
METEOBLUE_API_KEY = os.getenv("METEOBLUE_API_KEY", "")


def fetch_open_meteo():
    """Fetch weather data from Open-Meteo (No API key required)"""
    url = "https://api.open-meteo.com/v1/forecast"

    # Params a dictionary , requests attaches these to the end of the URL
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current_weather": True,
        "timezone": "auto"
    }
    # for error handling , network call, if internet drops or server fails wont crash
    # triggers except block if 404 not found or 500 server error
    #trnslates the raw text response into a structures python dictionary so values can be extracted directly
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()["current_weather"]
        return {"temp_c": data["temperature"], "wind_speed": data["windspeed"]}
    except Exception as e:
        return {"error": str(e)}

def fetch_openweather():
    """Fetch weather data from OpenWeatherMap"""
    if not OPENWEATHER_API_KEY:
        return {"error": "Missing API Key"}
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": LATITUDE, "lon": LONGITUDE, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        res = requests.get(url, params=params, timeout=10).json()
        return {"temp_c": res["main"]["temp"], "wind_speed": res["wind"]["speed"]}
    except Exception as e:
        return {"error": str(e)}

def fetch_weatherapi():
    """Fetch weather data from WeatherAPI.com"""
    if not WEATHERAPI_KEY:
        return {"error": "Missing API Key"}
    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": WEATHERAPI_KEY, "q": f"{LATITUDE},{LONGITUDE}"}
    try:
        res = requests.get(url, params=params, timeout=10).json()
        return {"temp_c": res["current"]["temp_c"], "wind_speed": res["current"]["wind_kph"]}
    except Exception as e:
        return {"error": str(e)}

def fetch_tomorrow():
    """Fetch weather data from Tomorrow.io"""
    if not TOMORROW_API_KEY:
        return {"error": "Missing API Key"}
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={LATITUDE},{LONGITUDE}&apikey={TOMORROW_API_KEY}"
    try:
        res = requests.get(url, timeout=10).json()
        vals = res["data"]["values"]
        return {"temp_c": vals["temperature"], "wind_speed": vals["windSpeed"]}
    except Exception as e:
        return {"error": str(e)}

def fetch_meteoblue():
    """Fetch weather data from meteoblue"""
    if not METEOBLUE_API_KEY:
        return {"error": "Missing API Key"}
    url = f"https://my.meteoblue.com/packages/basic-1h_basic-day?lat={LATITUDE}&lon={LONGITUDE}&apikey={METEOBLUE_API_KEY}"
    try:
        res = requests.get(url, timeout=10).json()
        # Takes first hourly data point
        return {"temp_c": res["data_1h"]["temperature"][0], "wind_speed": res["data_1h"]["windspeed"][0]}
    except Exception as e:
        return {"error": str(e)}

# saving logs to a csv file
def log_data():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Run all API requests
    results = {
        "Timestamp": timestamp,
        "OpenMeteo_Temp": fetch_open_meteo().get("temp_c", "N/A"),
        "OpenWeather_Temp": fetch_openweather().get("temp_c", "N/A"),
        "WeatherAPI_Temp": fetch_weatherapi().get("temp_c", "N/A"),
        "TomorrowIO_Temp": fetch_tomorrow().get("temp_c", "N/A"),
        "MeteoBlue_Temp": fetch_meteoblue().get("temp_c", "N/A")
    }

    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(results)

    print(f"[{timestamp}] Successfully logged weather data to {CSV_FILE}")

if __name__ == "__main__":
    log_data()