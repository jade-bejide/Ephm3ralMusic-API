from datetime import date
from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
    albums: List[Album]
    songs: List[Song]
    total_playtime: int
    user_score: Optional[float] = None

class System(BaseModel):
    artists: List[Artist]
    songs: List[Song]
    artistIDTracker: int
    songIDTracker: int
    genreIDTracker: int
    albumIDTracker: int


system = System(artists=[], 
                songs=[], 
                artistIDTracker=0, 
                songIDTracker=0,
                genreIDTracker=0,
                albumIDTracker=0)

#helper functions
def getArtistOnId(id):
    relArtist = None
    for artist in system.artists:
        if artist.id == id:
            relArtist = artist
            break

    return relArtist

def getSongOnId(id):
    relSong = None
    for song in system.songs:
        if song.id == id:
            relSong = song
            break
    
    return relSong

#crud operations

@app.get("/")
def read_root():
    artistNames = list(map(lambda artist: artist.name, system.artists))
    return {"artists": artistNames}

@app.get("/artist/{artist_id}")
def get_artist(artist_id: int):
    artist=getArtistOnId(artist_id)

    return {"Artist": artist}

@app.post("/artists/{artist_id}")
def add_artist(name: str):
    system.artistIDTracker += 1
    artist = Artist(id=system.artistIDTracker, 
                    name=name, 
                    albums=[], 
                    songs=[], 
                    total_playtime=0, 
                    user_score=None
                )

    
    system.artists.append(artist)

    return {"artist_name": artist.name, "artist_id": artist.id}

@app.delete("/artist/{artist_id")
def delete_artist(artist_id: int, artist: Artist):
    return {"artist_name": artist.name, "artist_id": artist_id}

@app.post("/artists/{artist_id}/{song_id}")
def add_song_to_artist(artist_id: int, name: str, genres: List[Genre], duration: int, listens: int):
    system.songIDTracker += 1
    song = Song(id=system.songIDTracker,
                name=name,
                genres=genres,
                duration=duration,
                listens=listens
            )

    
    system.songs.append(song)

    #get artist to add song to based on id
    artist = getArtistOnId(artist_id)

    artist.songs.append(song)

    return {"artist_name": artist.name, "artist_id": artist.id, "song_name": song.name, "song_id": song.id}

    

