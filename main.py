from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080"
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
    return {"Ephm3ralMusic-API": "Home"}
