import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import dataobjects

#sql stuff
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Enum, Float, DateTime
from database.database import Base, meta, db_engine
import enum

#need to add not null as appropriate 
class Artists(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    total_playtime = Column(Integer)
    user_score = Column(Float)

class Albums(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    release_date = Column(DateTime)
    listens = Column(Integer)
    total_playtime = Column(Integer)
    user_score = Column(Float)

class AlbumsByArtists(Base):
    __tablename__ = "albumsByArtists"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey(Artists.id), primary_key=True)

class Songs(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    artist_id = Column(Integer, ForeignKey(Artists.id))
    album_id = Column(Integer, ForeignKey(Albums.id))
    duration = Column(Integer)
    listens = Column(Integer)
    user_score = Column (Float)

class Genres(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    avg_listeners = Column(Float)
    avg_score = Column(Float)

class SongByGenre(Base):
    __tablename__ = "songByGenre"

    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey(Songs.id), primary_key=True)
    

# class AlbumBySongs(Base):
#     __tablename__ = "albumBySongs"

#     album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
#     song_id = Column(Integer, ForeignKey(Songs.id), primary_key=True)

class AlbumByGenres(Base):
    __tablename__ = "albumByGenres"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True)

meta.create_all(db_engine)








