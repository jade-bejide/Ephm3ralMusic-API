import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'your_clientid'
secret = 'your_secret'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_sp():
    return sp