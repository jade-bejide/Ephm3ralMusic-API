from typing import List
from sqlalchemy.orm import Session
from exceptions import ArtistAlreadyInSystemError, ArtistNotFoundError, \
 AlbumAlreadyInSystemError, AlbumNotFoundError, \
    GenreAlreadyInSystemError, GenreNotFoundError, \
    SongAlreadyInSystemError, SongNotFoundError
from models import Artists, Albums, Songs, Genres, SongByGenre, AlbumByGenres, AlbumBySongs
from schemas import Artists, Albums, Songs, Genres

def get_all_artists(session: Session, limit: int, offset: int) -> List[Artists]:
    return session.query(Artists).offset(offset).limit(limit).all()

def get_artist_by_id(session: Session, _id: int) -> Artists:
    artist = session.query(Artists).get(_id)

    if artist is None:
        raise ArtistNotFoundError

    return artist

def add_artist(session: Session, artist: Artist) -> Artists:
    artist_details = session.query(Artists).filter(Artists.id == artist.id)

    if artist_details is not None:
        raise ArtistAlreadyInSystemError

    new_artist = Artists(**artist.dict())
    session.add(new_artist)
    session.commit()
    session.refresh(new_artist)
    return new_artist

def update_artist_info(session: Session, _id: int, info_update: Artist) -> Artists:
    artist_details = get_artist_by_id(session, _id)

    if artist_details is None:
        raise ArtistNotFoundError

    artist_details.name = info_update.name
    artist_details.albums = info_update.albums
    artist_details.songs = info_update.songs
    artist_details.total_playtime = info_update.total_playtime
    artist_details.user_score = info_update.user_score 