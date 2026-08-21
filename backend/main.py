from fastapi import FastAPI 
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from services.weather import get_weather

from services.gemini import gemini_recom, ask_gemini

from services.retrieval import embed_query, retrieve_embed

from services.index import index_doc, record1

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OW_API_KEY")

if API_KEY is None:
    raise RuntimeError("openweather API not found in .env")

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

class queryINP(BaseModel):
    query : str


def give_prc(crop):
    return prices[crop]

@app.post('/recom')
def recommend(uin : inpc):
    weather = get_weather(uin.city)

    gemop = gemini_recom(weather, uin.crop)

    return gemop

@app.post('/query')
def answer(uin : queryINP):

    winner_chunk = retrieve_embed(uin.query, record1)

    answer = ask_gemini(uin.query, winner_chunk)

    return answer

    








