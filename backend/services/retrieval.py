from google import genai

from dotenv import load_dotenv

import os

load_dotenv()

API_KEY = os.getenv("GEM_API_KEY")

import math

def cos_check(v1, v2):
    dot = 0
    for a, b in zip(v1, v2):
        dot += a*b

    mag1 = math.sqrt(sum(x**2 for x in v1))
    mag2 = math.sqrt(sum(x**2 for x in v2))

    return dot / (mag1 * mag2)


client = genai.Client(api_key = API_KEY)

def embed_query(query): 
    query_embed = client.models.embed_content(
        model = "gemini-embedding-001",
        contents = query
    )

    return query_embed.embeddings[0].values


def retrieve_embed(query, all_embeds):
    max_cos = -1
    closest_chunk = ""

    embedded_query = embed_query(query)

    for i in all_embeds:
        temp_cos = cos_check(embedded_query, i["embedding"])
        if temp_cos > max_cos:
            max_cos = temp_cos
            closest_chunk = i

    return closest_chunk

