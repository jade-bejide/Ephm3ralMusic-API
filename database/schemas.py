from pydantic import BaseModel
from typing import List, Optional


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from main import Artist, Album, Song, Genre

class Artists(Artist):
    class Config:
        orm_mode = True

class PaginatedArtistsInfo(Artists):
    limit: int
    offset: int
    data: List[Artists]

class Albums(Album):
    class Config:
        orm_mode = True

class PaginatedAlbumsInfo(Albums):
    limit: int
    offset: int
    data: List[Albums]

class Songs(Song):
    class Config:
        orm_mode = True

class PaginatedSongsInfo(Songs):
    limit: int
    offset: int
    data: List[Songs]

class Genres(Genre):
    class Config:
        orm_mode = True

class PaginatedGenresInfo(Genres):
    limit: int
    offset: int
    data: List[Genres]
    

