import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Spotify Authentication
def spotify_authenticate():
    client_id = 'd4706f4329eb482b97895ff639479528'
    client_secret = '303a9cf3aa154194857bda5cd1a6ec7a'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    return sp

# Extract track info from Spotify playlist
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)
    while results:
        tracks.extend(results['items'])
        results = sp.next(results)
    return tracks

def extract_track_info(tracks):
    track_info = []
    for track in tracks:  # Assuming tracks is a list of track dictionaries
        track_info.append({
            'name': track['track']['name'],
            'artists': [artist['name'] for artist in track['track']['artists']]
        })
    return track_info

from google_auth_oauthlib.flow import InstalledAppFlow
import os

# YouTube Authentication
def youtube_authenticate():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Required for local testing
    client_secrets_file = '/Users/luisguinea/Documents/Pruebas/client_secret_779431023512-fk5dokvfftvvqoe3783tuc5nt66478os.apps.googleusercontent.com.json'
    
    # Define the scopes and redirect_uri
    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
    redirect_uri = 'http://localhost:8888/'  # Example redirect URI, adjust as needed

    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes, redirect_uri=redirect_uri)
    credentials = flow.run_local_server(port=8888)
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
    return youtube

# Initialize a cache dictionary for YouTube searches
youtube_search_cache = {}

# Search YouTube and add to playlist
def search_youtube(youtube, track_name, artist_name):
    search_key = f"{track_name} {artist_name}"
    if search_key in youtube_search_cache:
        print(f"Cache hit for: {search_key}")
        return youtube_search_cache[search_key]

    search_response = youtube.search().list(
        q=search_key,
        part="id,snippet",
        maxResults=1
    ).execute()

    if search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        print(f"Successfully found YouTube track: {track_name} by {artist_name}. Video ID: {video_id}")
        youtube_search_cache[search_key] = video_id
        return video_id
    else:
        print(f"No YouTube tracks found for: {track_name} by {artist_name}.")
        youtube_search_cache[search_key] = None
        return None

def create_or_get_playlist(youtube, playlist_name, playlist_description=""):
    playlists_response = youtube.playlists().list(
        part="snippet",
        mine=True,
        maxResults=50
    ).execute()

    for playlist in playlists_response['items']:
        if playlist['snippet']['title'] == playlist_name:
            return playlist['id']

    create_response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": playlist_description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    ).execute()

    return create_response['id']

# Main execution
if __name__ == "__main__":
    playlist_id = '37i9dQZF1DXb0AsvHMF4aM'
    sp = spotify_authenticate()
    tracks = get_playlist_tracks(sp, playlist_id)
    track_info = extract_track_info(tracks)

    youtube = youtube_authenticate()
    youtube_playlist_id = create_or_get_playlist(youtube, "Your YouTube Playlist Name", "Your playlist description")

    for info in track_info:
        video_id = search_youtube(youtube, info['name'], ', '.join(info['artists']))
        if video_id:
            # Add video to playlist code goes here
            pass