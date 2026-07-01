from fastapi import FastAPI 
from pydantic import BaseModel
import requests

from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
genai.configure(api_key = os.getenv("GEM_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

API_KEY = os.getenv("OW_API_KEY")

if API_KEY is None:
    raise RuntimeError("openweather API not found in .env")

crop_base = {
    'rice' : {"temp" : [21,37], "humidity" : [80,85]},
    'maize' : {"temp" : [21, 27], "humidity" : [50, 80]}, 
    'wheat' : {"temp" : [12, 25], "humidity" : [50, 60]}
}

prices = {
    'rice' : 2400,
    'maize' : 1800,
    'wheat' : 2000
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


class inpc(BaseModel):
    city : str
    crop : str

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    resp = requests.get(url)

    if resp.status_code != 200:
        return 'invalid input'

    data = resp.json()

    temp = data['main']['temp']
    hum = data['main']['humidity']
    weather = data['weather'][0]['description']

    return temp, hum, weather

def gen_adv(temp, hum, crop, weather, price):

    prompt = f"""
    You are an agriculturad advisor. provide concise and actionable advice based on the 
    following data (get straight to the advice, and structure your response) = 
    temperature : {temp},
    humidity : {hum},
    weather : {weather}
    crop : {crop},
    current market price : {price} per quintal.
    """

    response = model.generate_content(prompt)

    return response.text

def give_prc(crop):
    return prices[crop]

@app.post('/recom')
def recommend(uin : inpc):
    temp, hum, weather = get_weather(uin.city)
    price = give_prc(uin.crop)

    return gen_adv(temp, hum, uin.crop, weather, price)







