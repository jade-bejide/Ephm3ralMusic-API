from pydantic import BaseModel
from typing import List, Optional


import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from dataobjects import Artist, Album, Song, Genre

#data validation and conversion
class ArtistInfo(Artist):
    class Config:
        orm_mode = True

class PaginatedArtistsInfo(ArtistInfo):
    limit: int
    offset: int
    data: List[ArtistInfo]

class Albums(Album):
    class Config:
        orm_mode = True

class PaginatedAlbumsInfo(Albums):
    limit: int
    offset: int
    data: List[Albums]

class SongsInfo(Song):
    class Config:
        orm_mode = True

class PaginatedSongsInfo(SongsInfo):
    limit: int
    offset: int
    data: List[SongsInfo]

class Genres(Genre):
    class Config:
        orm_mode = True

class PaginatedGenresInfo(Genres):
    limit: int
    offset: int
    data: List[Genres]
    

