from pypdf import PdfReader
from dotenv import load_dotenv
import os

from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("GEM_API_KEY")

from google import genai

client = genai.Client(api_key = API_KEY)

# class record(BaseModel):
#     text : str
#     page_no : int
#     pdf_source : str
#     embedding : list
#     chunk_id : int

def load_doc(pdfpath):

    pgList = []
    pgno = 0

    reader = PdfReader(pdfpath)

    for page in reader.pages:
        text = page.extract_text()
        pgList.append({"text" : text, "page" : pgno+1, "source" : pdfpath, "chunk_id" : pgno+1})
        pgno+=1

    return pgList

# def chunk_text(page_list):

#     chunks = []

#     for i in page_list:
#         chunk = ""
#         chunk = i["text"]
#         chunks.append(chunk)

#     return chunks

def embed_chunks(records):

    for record in records:
        resp = client.models.embed_content(
            model = "gemini-embedding-001",
            contents = record
        )

        record["embedding"] = resp.embeddings[0].values

    return records

def index_doc(pdfpath):
    load_list = load_doc(pdfpath)

    metaRecords = embed_chunks(load_list)

    return metaRecords


record1 = index_doc("backend\\data\\rice_science.pdf")



