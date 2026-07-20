from dotenv import load_dotenv
import os
import requests

load_dotenv()

from backend.main import inpc

API_KEY = os.getenv("OW_API_KEY")

params = {"city" : city}

def get_weather(city):
    resp = requests.get(
        url = f"http://api.openweathermap.org/data/2.5/weather", 

        params = {
            "q" : city, 
            "appid" : API_KEY,
            "units" : "metric"
        }
    )

    data = resp.json()

    temp = data["main"]["temp"]
    hum = data["main"]["humidity"]
    weather = data["weahter"]["description"]

    return {
        "temp" : temp, 
        "humidity" : hum,
        "weather" : weather
    }


