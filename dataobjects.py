from datetime import date
from typing import Optional, List
from pydantic import BaseModel

#setting up objects
class Genre(BaseModel):
    id: int
    name: str
    avg_listeners: Optional[float] = None
    avg_score: Optional[float] = None

class Song(BaseModel):
    id: int
    name: str
    genres: List[Genre]
    duration: int
    listens: int

class Album(BaseModel):
    id: int
    name: str
    release_date: date
    genres: List[Genre]
    songs: List[Song]
    #need to find a way to deal with this cyclic dependency
    #artist: Artist
    listens: int
    total_playtime: int
    user_score: Optional[float] = None

class Artist(BaseModel):
    id: int
    name: str
    # albums: List[Album]
    # songs: List[Song]
    total_playtime: int
    user_score: Optional[float] = None
    

