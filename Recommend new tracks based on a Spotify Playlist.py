# Import all the tracks from a Spotify playlist and extract track information.
# Recommend new tracks, based on Playlist.

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials and playlist ID
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/'
playlist_id = '3Ucav8aYcJW3JVvNAP4H1o'  # Corrected playlist ID

# Scopes required for reading a user's playlist
scope = 'playlist-read-private'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def get_playlist_tracks(playlist_id):
    """
    Fetch tracks from the specified Spotify playlist.
    """
    tracks = []
    results = sp.playlist_items(playlist_id)
    while results:
        tracks.extend(results['items'])
        results = sp.next(results)
    return tracks

def extract_track_info(tracks):
    """
    Extract track name and artist(s) from the playlist's tracks.
    """
    track_info = []
    for track in tracks:
        track_name = track['track']['name']
        artists = [artist['name'] for artist in track['track']['artists']]
        track_info.append({'name': track_name, 'artists': artists})
    return track_info

# Fetch and extract track information
tracks = get_playlist_tracks(playlist_id)
track_info = extract_track_info(tracks)

# Example usage: print the names and artists of the first few tracks
for info in track_info[:5]:
    print(f"Track: {info['name']} - Artists: {', '.join(info['artists'])}")

def get_audio_features_for_tracks(tracks):
    """
    Fetch audio features for each track in the playlist.
    """
    track_ids = [track['track']['id'] for track in tracks]
    features_list = sp.audio_features(track_ids)
    return features_list

def recommend_tracks_based_on_playlist(playlist_id, limit=20):
    """
    Recommend tracks based on the audio features of the tracks in a playlist.
    """
    tracks = get_playlist_tracks(playlist_id)
    features_list = get_audio_features_for_tracks(tracks)
    
    # Example: Use the first track's features as a seed. In practice, you might average features or choose differently.
    seed_features = features_list[0]
    
    # Assuming we're using the first track's ID as a seed. Adjust according to your strategy.
    seed_track_id = [tracks[0]['track']['id']]
    
    # Get recommendations based on the seed track
    recommendations = sp.recommendations(seed_tracks=seed_track_id, limit=limit)
    
    recommended_tracks = [recommendation['name'] for recommendation in recommendations['tracks']]
    return recommended_tracks

# Example usage
playlist_id = '3Ucav8aYcJW3JVvNAP4H1o'  # Use your playlist ID
recommended_tracks = recommend_tracks_based_on_playlist(playlist_id)
print("Recommended Tracks:", recommended_tracks)
