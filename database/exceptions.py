class ArtistException(Exception):
    ...

class ArtistNotFoundError(ArtistException):
    def __init__(self):
        self.status_code = "404"
        self.detail = "Artist is Not On The System"

class ArtistAlreadyInSystemError(ArtistException):
    def __init__(self):
        self.status_code = "409"
        self.detail = "Artist Already On System"

class AlbumException(Exception):
    ...

class AlbumNotFoundError(AlbumException):
    def __init__(self):
        self.status_code = "404"
        self.detail = "Album is Not On The System"

class AlbumAlreadyInSystemError(AlbumException):
    def __init__(self):
        self.status_code = "409"
        self.detail = "Album Already On System"

class GenreException(Exception):
    ...

class GenreNotFoundError(GenreException):
    def __init__(self):
        self.status_code = "404"
        self.detail = "Genre is Not On The System"

class GenreAlreadyInSystemError(GenreException):
    def __init__(self):
        self.status_code = "409"
        self.detail = "Genre Already On System"

class SongException(Exception):
    ...

class SongNotFoundError(SongException):
    def __init__(self):
        self.status_code = "404"
        self.detail = "Song is Not On The System"

class SongAlreadyInSystemError(SongException):
    def __init__(self):
        self.status_code = "409"
        self.detail = "Song Already On System"



