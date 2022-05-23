import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'client_id'
secret = 'client_secret'
#predefine username or ask for user to input
username = 'username'
#read ALL playlists
thescope = 'playlist-read-private'
#local development
redirecturi = 'http://localhost:8080/'

token = util.prompt_for_user_token(username,scope=thescope,client_id=client_id,client_secret=secret, redirect_uri=redirecturi)

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
sp = spotipy.Spotify(auth=token)

def get_sp():
    return sp

def get_sp():
    return sp