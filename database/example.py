from spotifyconnection import getPlaylistURLs
from database.spotifycredentials import get_sp

sp = get_sp()

jadesPlaylists = sp.user_playlists('jadesolaaaaa')['items']

getPlaylistURLs(jadesPlaylists)
