from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import api

app = FastAPI()
app.include_router(api.router)

#GET operation at root
@app.get('/')
def root():
    return {"Ephm3ralMusic-API": "Insert welcome message here"}