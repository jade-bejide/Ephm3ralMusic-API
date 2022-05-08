from base64 import encode
from fastapi import APIRouter, Depends, HTTPException, FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
import hashlib
import json
from objecttojson import serialiseObjectList

#Encrytpion
from cryptography.fernet import Fernet
from encryption.aescipher import get_key

from database.crud import get_all_artists, get_artist_by_id, add_artist_info, update_artist_info, delete_artist_info, add_cookie
from database.database import get_db
from database.exceptions import ArtistException
from database.models.schemas import ArtistInfo, PaginatedArtistsInfo
from dataobjects import Artist

app = FastAPI()
router = InferringRouter()

key = Fernet(get_key())

@cbv(router)
class System:
    session: Session = Depends(get_db)

    #API to get the list of artists info

    @router.get("/artists")
    def list_artists(self, limit: int = 10, offset: int = 0):
        artist_list = get_all_artists(self.session, limit, offset)
        
        responseContent = {"limit": limit, "offset": offset, "data": serialiseObjectList(artist_list)}
        response = JSONResponse(content=responseContent)
        self.create_cookie(response, responseContent)
        return response

    @router.post("/cookie/")
    def create_cookie(self, response: Response, msg: str):
        en = str(key.encrypt(str.encode(json.dumps(msg))))
        en = en[2:len(en)]
        add_cookie(self.session, en, get_key())
        response.set_cookie(key="ephm3ralmusic", value=en, domain="127.0.0.1:8000")
        return response

    #API to get artist based on id
    @router.get("/artist/{artist_id}")
    def get_artist(self, artist_id: int):
        try: 
            artist = get_artist_by_id(self.session, artist_id)

            response = JSONResponse(content=artist.as_dict())
            self.create_cookie(response, artist.as_dict())
            return response
        except:
            return {"Error": "Artist Not Found"}

    # API endpoint to add an artist info to the database

    @router.post("/artists")
    def add_artist(self, artist_info: Artist):
        try:
            artist_info = add_artist_info(self.session, artist_info)
            return artist_info
        except ArtistException as ae:
            raise HTTPException(**ae.__dict__)

    # API to update an existing artist info
    @router.put("/artist/{artist_id}", response_model=ArtistInfo)
    def update_artist(self, artist_id: int, new_info: Artist, session: Session=Depends(get_db)):
        try:
            artist_info = update_artist_info(self.session, artist_id, new_info)
            return artist_info
        except ArtistException as ae:
            raise HTTPException(**ae.__dict__)

    # API to delete an artist from the database
    @router.delete("/artist/{artist_id}")
    def delete_artist(self, artist_id: int, session: Session=Depends(get_db)):
        try:
            return delete_artist_info(self.session, artist_id)
        except ArtistException as ae:
            return HTTPException(**ae.__dict__)
