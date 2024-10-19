import os
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Spotify API credentials
SPOTIPY_CLIENT_ID = '523845d27c624a12b04290f3089bfc68'
SPOTIPY_CLIENT_SECRET = 'cc8c969c977d4a51a8dbe8204751f74b'

# Function to get Spotify access token
def get_spotify_access_token():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

# Function to extract track ID from Spotify URL
def extract_track_id(spotify_url):
    return spotify_url.split("/")[-1].split("?")[0]

# Function to get track details by track ID
def get_track_by_id(sp, track_id):
    return sp.track(track_id)

# Function to download artwork
def download_artwork(url):
    response = requests.get(url, stream=True)
    return response.content

# Main function
def main():
    spotify_url = input('Enter the Spotify URL: ')

    sp = get_spotify_access_token()
    track_id = extract_track_id(spotify_url)
    track = get_track_by_id(sp, track_id)

    if track:
        artwork_url = track['album']['images'][0]['url']
        artwork_content = download_artwork(artwork_url)

        # Create directory for artwork
        directory = '/Users/luisguinea/Downloads'
        os.makedirs(directory, exist_ok=True)
        
        # Create directory with track and artist name
        track_artist_directory = os.path.join(directory, f'{track["name"]} - {track["artists"][0]["name"]}')
        os.makedirs(track_artist_directory, exist_ok=True)
        
        # Save artwork in the new directory
        artwork_path = os.path.join(track_artist_directory, 'artwork.jpg')
        
        with open(artwork_path, 'wb') as f:
            f.write(artwork_content)

        print('Artwork downloaded successfully.')
    else:
        print('Track not found.')

if __name__ == '__main__':
    main()