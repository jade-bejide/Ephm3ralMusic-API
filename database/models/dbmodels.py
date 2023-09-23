import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Enum, Float, DateTime, Text
from db import Base, meta, db_engine
from models.baseModel import Model
import enum

# each model displays multiple inheritance from Base and Model
# add not null as appropriate
class Artists(Base, Model):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    total_playtime = Column(Integer)
    user_score = Column(Float)
    cover = Column(String(255))

class Cookies(Base, Model):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    cookie_content = Column(Text)
    cookie_key = Column(Text)



class Albums(Base, Model):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    release_date = Column(String(255))
    listens = Column(Integer)
    total_playtime = Column(Integer)
    user_score = Column(Float)
    artist_id = Column(Integer, ForeignKey(Artists.id))
    cover = Column(String(255))


#Potentially unnecessary
class AlbumsByArtists(Base, Model):
    __tablename__ = "albumsByArtists"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey(Artists.id), primary_key=True)

class Songs(Base, Model):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    artist_id = Column(Integer, ForeignKey(Artists.id))
    #album_id = Column(Integer, ForeignKey(Albums.id))
    duration = Column(Integer)
    listens = Column(Integer)
    user_score = Column (Float)
    cover = Column(String(255))

class Genres(Base, Model):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    avg_listeners = Column(Float)
    avg_score = Column(Float)



class SongByGenre(Base, Model):
    __tablename__ = "songByGenre"

    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey(Songs.id), primary_key=True)
    

class AlbumBySongs(Base, Model):
    __tablename__ = "albumBySongs"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey(Songs.id), primary_key=True)

class AlbumByGenres(Base, Model):
    __tablename__ = "albumByGenres"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True)

class ArtistByGenres(Base, Model):
    __tablename__ = "artistByGenres"

    artist_id = Column(Integer, ForeignKey(Artists.id), primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True)

meta.create_all(db_engine)








