from google import genai
from dotenv import load_dotenv

import json

import os

load_dotenv()

client = genai.Client(api_key = os.getenv("GEM_API_KEY"))

def ask_gemini(context):
    resp = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = context
    )

    data = json.loads(resp.text)

    return data

