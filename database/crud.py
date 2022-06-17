from typing import List
from fastapi import Cookie
from sqlalchemy.orm import Session, Query
from database.exceptions import ArtistAlreadyInSystemError, ArtistNotFoundError, \
 AlbumAlreadyInSystemError, AlbumNotFoundError, \
    GenreAlreadyInSystemError, GenreNotFoundError, \
    SongAlreadyInSystemError, SongNotFoundError
from database.models.dbmodels import Artists, Albums, Songs, Genres, SongByGenre, AlbumByGenres, AlbumBySongs, Cookies
from database.models.schemas import ArtistInfo, AlbumsInfo, SongsInfo, Genres

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
    #session.refresh(new_artist)
    return new_artist

#may want to separate this into separate updations per field
def update_artist_info(session: Session, _id: int, info_update: Artist) -> ArtistInfo:
    artist_details = get_artist_by_id(session, _id)

    if artist_details is None:
        raise ArtistNotFoundError

    artist_details.name = info_update.name
    # artist_details.albums = info_update.albums
    # artist_details.songs = info_update.songs
    artist_details.total_playtime = info_update.total_playtime
    artist_details.user_score = info_update.user_score 

    session.commit()
    session.refresh(artist_details)

    return artist_details

# def add_album_to_artist(session)

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
    single_details = get_song_by_id(session, _id)
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

    