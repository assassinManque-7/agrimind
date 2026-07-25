from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

import json

import os
import json

load_dotenv()

class gemo(BaseModel):
    adv : str
    reason : str
    confidence : int

client = genai.Client(api_key = os.getenv("GEM_API_KEY"))

def gemini_recom(context, crop):
    cont = json.dumps(context, indent = 2)

    prompt = f"""You are an agricultural expert. 

    generate farming advice for {crop} based on the following context only.
    
    in the absence of any important info, express your uncertainty rather than making assumptions.
    
    provide your reasoning and a confidence score for your recommendations.
    
    context : {cont}"""

    resp = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt,
        config = genai.types.GenerateContentConfig(
            response_mime_type = "application/json",
            response_schema = gemo,
        ),
    )

    data = json.loads(resp.text)

    return data

def ask_gemini(query, retrieved_chunk):
    prompt = f"""you are an agricultural expert. generate a response to the given farmer query using information that you're sure of, rather
    than making assumptions. also ensure that you're faithful to the context provided - 
    query : {query}
    context : {retrieved_chunk} """

    resp = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = prompt,
    )

    return resp.text