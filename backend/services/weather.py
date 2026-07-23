from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OW_API_KEY")

def get_weather(city):
    resp = requests.get(
        url = f"http://api.openweathermap.org/data/2.5/weather/", 

        params = {
            "q" : city, 
            "appid" : API_KEY,
            "units" : "metric"
        }
    )

    data = resp.json()

    temp = data["main"]["temp"]
    hum = data["main"]["humidity"]
    weather = data["weather"][0]["description"]

    return {
        "temp" : temp, 
        "humidity" : hum,
        "weather" : weather
    }


