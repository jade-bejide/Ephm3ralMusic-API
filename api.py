from base64 import encode
from tempfile import TemporaryFile
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

from database.crud import add_single, get_all_albums_by_artistId, get_all_artists, get_genre_from_artist, get_genres, get_genres_from_artist, get_single_by_id, get_all_songs, get_all_songs_by_artist_id, get_artist_by_id, add_artist_info, update_artist_info, delete_artist_info, add_cookie, get_all_albums
from database.db import get_db
from database.exceptions import ArtistException, ArtistGenreError, NoGenresInSystem, SongException
from database.models.schemas import ArtistInfo, PaginatedArtistsInfo
from dataobjects import Artist, Song

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

    @router.get("/songs")
    def get_all_songs(self, limit = 10, offset = 0):
        try:
            songs = get_all_songs(self.session, limit, offset)

            return JSONResponse(serialiseObjectList(songs))

        except:
            return {"Error": "Could not get songs"}

    @router.get("/albums")
    def get_all_albums(self, limit = 10, offset = 0):
        try:
            albums = get_all_albums(self.session, limit, offset)
            print(serialiseObjectList(albums))

            return JSONResponse(content=serialiseObjectList(albums))

        except:
            return {"Error": "Could not get albums"}

    @router.get("/artist/{artist_id}/albums")
    def get_all_albums_by_artist(self, artist_id):
        try:
            albums = get_all_albums_by_artistId(self.session, artist_id)
            

            return JSONResponse(content=serialiseObjectList(albums))
        except:
            return {"Error": "Could not find songs from artist"}

    @router.get("/song/{song_id}")
    def get_song_by_id(self, song_id: int):
        try:
            song = get_single_by_id(self.session, song_id)

            return JSONResponse(content=song.as_dict())
        except:
            return {"Error": "Song Not Found"}

    @router.get("/artist/{artist_id}/songs")
    def get_songs_by_artist(self, artist_id: int):
        try:
            songs = get_all_songs_by_artist_id(self.session, artist_id)
            response = JSONResponse(content=serialiseObjectList(songs))
            return response
        except:
            return {"Error": "Artist Not Found So Cannot Deliver Songs"}

    @router.post("/songs")
    def add_song(self, song_info: Song):
        try:
            song_info = add_single(self.session, song_info)
            return song_info
        except SongException as se:
            raise HTTPException(**se.__dict__)

    
    

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

    #API endpoint for genre related calls

    @router.get("/genres")
    def get_all_genres(self, session: Session=Depends(get_db)):
        try:
            return get_genres(self.session)
        except NoGenresInSystem as ge:
            return HTTPException(**ge.__dict__)

    @router.get("/artist/{artist_id}/genres")
    def get_all_genres_by_artist(self, artist_id: int, session: Session=Depends(get_db)):
        try:
            return get_genres_from_artist(self.session, artist_id)
        except ArtistGenreError as age:
            return HTTPException(**age.__dict__)

    @router.get("/artist/{artist_id}/genres/{genre_id}")
    def get_genre_by_artist(self, artist_id: int, genre_id: int, session: Session=Depends(get_db)):
        try:
            return get_genre_from_artist(self.session, artist_id, genre_id)
        except ArtistGenreError as age:
            return HTTPException(**age.__dict__)
