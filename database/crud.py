from typing import List
from sqlalchemy.orm import Session
from database.exceptions import ArtistAlreadyInSystemError, ArtistNotFoundError, \
 AlbumAlreadyInSystemError, AlbumNotFoundError, \
    GenreAlreadyInSystemError, GenreNotFoundError, \
    SongAlreadyInSystemError, SongNotFoundError
from database.models import Artists, Albums, Songs, Genres, SongByGenre, AlbumByGenres, AlbumBySongs
from database.schemas import ArtistInfo, Albums, Songs, Genres

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from dataobjects import Artist

def get_all_artists(session: Session, limit: int, offset: int) -> List[Artist]:
    return session.query(Artists).offset(offset).limit(limit).all()

def get_artist_by_id(session: Session, _id: int) -> Artists:
    artist = session.query(Artists).get(_id)

    if artist is None:
        raise ArtistNotFoundError

    return artist

def add_artist_info(session: Session, artist: Artist) -> Artists:
    artist_details = session.query(Artists).filter(Artists.id == artist.id).first()

    if artist_details is not None:
        raise ArtistAlreadyInSystemError


    print(artist.dict())
    sql_keys = ['id', 'name', 'total_playtime', 'user_score']
    artistDict = {x:artist.dict()[x] for x in sql_keys}
    print(artistDict)

    new_artist = Artists(**artistDict)
    session.add(new_artist)
    session.commit()
    #session.refresh(new_artist)
    return new_artist

#may want to separate this into separate updations per field
def update_artist_info(session: Session, _id: int, info_update: Artist) -> ArtistInfo:
    artist_details = get_artist_by_id(session, _id)

    if artist_details is None:
        raise ArtistNotFoundError

    artist_details.name = info_update.name
    artist_details.albums = info_update.albums
    artist_details.songs = info_update.songs
    artist_details.total_playtime = info_update.total_playtime
    artist_details.user_score = info_update.user_score 

    session.commit()
    session.refresh(artist_details)

    return artist_details

# def add_album_to_artist(session)

def delete_artist_info(session: Session, _id:int) -> Artists:
    
    artist_details = get_artist_by_id(session, _id)
    print("ID", artist_details.dict().id)
    print("Hello?")
    if artist_details is None:
        raise ArtistNotFoundError

    session.delete(artist_details)
    session.commit()

    return