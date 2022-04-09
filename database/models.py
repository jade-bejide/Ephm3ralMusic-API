import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import main

#sql stuff
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Enum, Float, DateTime
from database import Base
import enum

class Artists(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    total_playtime = Column(Integer)
    user_score = Column(Float)

class Albums(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    release_date = Column(DateTime)
    listens = Column(Integer)
    total_playtime = Column(Integer)
    user_score = Column(Float)

class Songs(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    artist_id = Column(Integer, ForeignKey(Artists.id))
    duration = Column(Integer)
    listens = Column(Integer)
    user_score = Column (Float)

class Genres(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    avg_listeners = Column(Float)
    avg_score = Column(Float)

class SongByGenre(Base):
    __tablename__ = "songByGenre"

    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey(Songs.id), primary_key=True)
    

class AlbumBySongs(Base):
    __tablename__ = "albumBySongs"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey(Songs.id), primary_key=True)

class AlbumByGenres(Base):
    __tablename__ = "albumBySongs"

    album_id = Column(Integer, ForeignKey(Albums.id), primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey(Genres.id), primary_key=True)








