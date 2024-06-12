from fastapi import FastAPI
from devmodules.userlib import *
from pydantic import BaseModel
app = FastAPI()
class Query(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"Assalamualaikum": "People! please visit localhost:8000/docs"}

@app.post("/ask")
# async def ask_question(query):
#     response = Ai_response(query)
#     return {"answer": response}

async def ask_question(query: Query):
    response = Ai_response(query.question)
    return {"answer": response}