from fastapi import FastAPI 
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from services.weather import get_weather

from services.gemini import ask_gemini

import os
from dotenv import load_dotenv
load_dotenv()

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



def give_prc(crop):
    return prices[crop]

@app.post('/recom')
def recommend(uin : inpc):
    weather = get_weather(uin.city)

    gemop = ask_gemini(weather, uin.crop)

    return gemop
    







