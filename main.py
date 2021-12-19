from collections import Counter
import os
from dotenv import load_dotenv

import spotipy
from spotipy import client
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = os.getenv('SCOPE')

PLAYLIST_ID = "0HY9RlNjxtyG7VxaeYecMT?si=8006a44fa0d64744"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                            client_secret=CLIENT_SECRET,
                                            redirect_uri=REDIRECT_URI,
                                            scope=SCOPE))

def get_artists(playlist):
    playlist = sp.playlist(playlist_id=playlist)

    artists = [artist for sublist in [track['track']['album']['artists'] for track in playlist['tracks']['items']] for artist in sublist]
    return artists

def get_artist_genres(artist):
    artist_detail = sp.artist(artist['external_urls']['spotify'])
    return artist_detail['genres']

def get_list_of_percentages(l):
    c = Counter(l)
    return [(i, c[i] / len(l) * 100.0) for i in c]

artists = get_artists(PLAYLIST_ID)
genres = [genre for sublist in [get_artist_genres(artist) for artist in artists] for genre in sublist]
percentage = get_list_of_percentages(genres)
sorted_list = sorted(percentage,key=lambda x:x[1],reverse=True)
print([item[0] for item in sorted_list[:3]])