from typing import List
from fastapi import Cookie
from sqlalchemy import select
from sqlalchemy.orm import Session, Query
from database.exceptions import ArtistAlreadyInSystemError, ArtistNotFoundError, \
 AlbumAlreadyInSystemError, AlbumNotFoundError, \
    GenreAlreadyInSystemError, GenreNotFoundError, \
    SongAlreadyInSystemError, SongNotFoundError
from database.models.dbmodels import ArtistByGenres, Artists, Albums, Songs, Genres, SongByGenre, AlbumByGenres, AlbumBySongs, Cookies
from database.models.schemas import ArtistInfo, AlbumsInfo, SongsInfo

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from dataobjects import Artist, Song, Album

def add_cookie(session: Session, cookie: Cookie, key: str) -> Cookie:
    cookie_dict = {
        "cookie_content": cookie,
        "cookie_key": str(key)
    }
    new_cookie = Cookies(**cookie_dict)
    session.add(new_cookie)
    session.commit()

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

    new_artist = Artists(**artist.dict())
    session.add(new_artist)
    session.commit()
    return new_artist

#may want to separate this into separate updations per field
def update_artist_info(session: Session, _id: int, info_update: Artist) -> ArtistInfo:
    artist_details = get_artist_by_id(session, _id)

    if artist_details is None:
        raise ArtistNotFoundError

    artist_details.name = info_update.name
    artist_details.total_playtime = info_update.total_playtime
    artist_details.user_score = info_update.user_score 

    session.commit()
    session.refresh(artist_details)

    return artist_details

def delete_artist_info(session: Session, _id:int) -> Artists:
    
    artist_details = get_artist_by_id(session, _id)
    if artist_details is None:
        raise ArtistNotFoundError

    session.delete(artist_details)
    session.commit()

    return

# songs

def get_single_by_id(session: Session, _id: int) -> Songs:
    single = session.query(Songs).get(_id)

    if single is None:
        raise SongNotFoundError

    return single

def get_all_songs(session: Session, limit:int, offset: int) -> List[Song]:
    return session.query(Songs).offset(offset).limit(limit).all()

def get_all_songs_by_artist_id(session: Session, _id:int) -> List[Song]:
    
    artist = session.query(Artists).get(_id)
    if artist is None:
        raise ArtistNotFoundError

    songs = session.query(Songs).filter_by(artist_id=_id).all()

    return songs

def delete_single(session: Session, song_id: int) -> Songs:
    single_details = get_single_by_id(session, song_id)
    if single_details is None:
        raise SongNotFoundError
    
    session.delete(single_details)
    session.commit()
    return

def add_single(session: Session, song: Song) -> Songs:
    song_details = session.query(Songs).filter_by(song.id)

    if song_details is not None:
        raise SongAlreadyInSystemError

    new_single = Songs(**song.dict())
    session.add(new_single)
    session.commit()

    return new_single

# albums
def get_all_albums(session: Session, limit: int, offset: int) -> List[Album]:
    return session.query(Albums).offset(offset).limit(limit).all()

def get_all_albums_by_artistId(session: Session, _id: int) -> List[Album]:

    artist = session.query(Artists).get(_id)
    if artist is None:
        raise ArtistNotFoundError

    return session.query(Albums).filter_by(artist_id=_id).all()

def get_album_id(session: Session, album_id: int) -> Album:
    return session.query(Albums).get(album_id)


def add_album_by_genres(session: Session, album: Album) -> AlbumByGenres:
    album_details = session.query(Albums).filter_by(album.id)
 
    if album_details is None:
        raise AlbumNotFoundError

    album_songs_ids = session.query(Songs).select_from(Song.id).filter_by(album.id)
    album_songs_ids_list = [song[0] for song in album_songs_ids]

    ##get all songs
    #get all songs by genre
    albumGenres = []
    for song in album_songs_ids_list:
        associatedGenres = session.query(SongByGenre).select_from(SongByGenre.genre_id).filter_by(song).all()
        associatedGenresList = [genre[0] for genre in associatedGenres]

        for genre in associatedGenresList:
            album_by_genre = AlbumByGenres(album.id, genre)
            session.add(album_by_genre)
            session.commit()


    return

def add_album(session: Session, album: Album) -> Albums:
    album_details = session.query(Albums).filter_by(album.id)

    if album_details is not None:
        raise AlbumAlreadyInSystemError

    new_album = Albums(**album.dict())
    session.add(new_album)
    session.commit()

    return new_album

#Genres

def get_genres(session: Session):
    genre_entries = session.query(Genres).all()

    return genre_entries

def get_genre_by_id(session: Session, genre_id: int):
    id = session.query(Genres).filter_by(id=genre_id).first()

    return id

def get_genres_from_artist(session: Session, artist_id: int, show_id: bool):
    genre_entries = session.query(ArtistByGenres).filter_by(artist_id=artist_id).all()


    if show_id: return genre_entries

    entries = []
    for entry in genre_entries:
        entry_dict = entry.__dict__
        entries.append(parse_genre_dict(session, entry_dict))

    return entries

def parse_genre_dict(session, genre_dict):
    named_entry = {}

    named_entry["artist"] = get_artist_by_id(session, genre_dict["artist_id"]).__dict__["name"]
    named_entry["genre"] = get_genre_by_id(session, genre_dict["genre_id"]).__dict__["name"]   

    return named_entry

def get_genre_from_artist(session: Session, artist_id: int, genre_id: int, show_id: bool):
    genre_entry = session.query(ArtistByGenres).filter_by(artist_id=artist_id, genre_id=genre_id).first()

    if show_id: return genre_entry
    return parse_genre_dict(session, genre_entry.__dict__)

    