from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database.crud import get_all_artists, get_artist_by_id, add_artist_info, update_artist_info, delete_artist_info
from database.database import get_db
from database.exceptions import ArtistException
from database.schemas import ArtistInfo, PaginatedArtistsInfo
from dataobjects import Artist

router = APIRouter()

@cbv(router)
class System:
    session: Session = Depends(get_db)

    #API to get the list of artists info

    @router.get("/artists", response_model=PaginatedArtistsInfo)
    def list_artists(self, limit: int = 10, offset: int = 0):
        artist_list = get_all_artists(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": artist_list}

        return response

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
    def update_artist(artist_id: int, new_info: Artist, session: Session=Depends(get_db)):
        try:
            artist_info = update_artist_info(session, artist_id, new_info)
            return artist_info
        except ArtistException as ae:
            raise HTTPException(**ae.__dict)

    # API to delete an artist from the database
    @router.delete("/artist/{artist_id}")
    def delete_artist(artist_id: int, session: Session=Depends(get_db)):
        try:
            print("ID", artist_id)
            return delete_artist_info(session, artist_id)
        except ArtistException as ae:
            print("Nah")
            return HTTPException(**ae.__dict__)
    