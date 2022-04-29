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

    @router.get("/artists")
    def list_artists(self, limit: int = 10, offset: int = 0):
        artist_list = get_all_artists(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": artist_list}

        return response

    #API to get artist based on id
    @router.get("/artist/{artist_id}")
    def get_artist(self, artist_id: int):
        artist = get_artist_by_id(self.session, artist_id)

        return artist

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
    