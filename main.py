from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:8080/artists",
    "http://127.0.0.1:8000/artists",
    "file://C:/Users/jades/Documents/Python%20Scripts/APIs/Ephm3ralMusic-API/examplewebpage.html"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#GET operation at root
@app.get('/')
def root():
    return {"Ephm3ralMusic-API": "Insert welcome message here"}