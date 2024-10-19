# %%
import requests
import base64
import pandas as pd

# Replace with your Spotify app credentials
CLIENT_ID = '523845d27c624a12b04290f3089bfc68'
CLIENT_SECRET = 'cc8c969c977d4a51a8dbe8204751f74b'

def get_spotify_token():
    """Get Spotify API token."""
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode('ascii'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    token_info = response.json()
    return token_info['access_token']

token = get_spotify_token()

# %%
# Search for the artist
def search_artist_spotify(artist_name, token):
    """Search for an artist on Spotify."""
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    if data['artists']['items']:
        return data['artists']['items'][0]
    else:
        raise ValueError("Artist not found")

artist_name = input("Enter the artist name: ")
artist = search_artist_spotify(artist_name, token)
artist_id = artist['id']
print(f"Artist ID: {artist_id}")

# %%
# Retrieve artist details

def get_artist_details(artist_id, token):
    """Retrieve detailed information about an artist."""
    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(artist_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_artist_albums(artist_id, token):
    """Retrieve all albums by the artist."""
    albums_url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(albums_url, headers=headers)
    response.raise_for_status()
    return response.json()

artist_details = get_artist_details(artist_id, token)
albums = get_artist_albums(artist_id, token)

print("Artist Details:")
print(f"Name: {artist_details['name']}")
print(f"Genres: {', '.join(artist_details['genres'])}")
print(f"Popularity: {artist_details['popularity']}")
print(f"Followers: {artist_details['followers']['total']}")

print("\nAlbums:")
for album in albums['items']:
    print(f" - {album['name']} ({album['release_date']})")

# %%
# Function to retrieve the Spotify URL for an album or track
def get_spotify_url(item):
    """Retrieve the Spotify URL for an album or track."""
    return item['external_urls']['spotify']

# Export to text file
def export_to_txt(file_path, artist_details, albums):
    """Export artist details and albums to a text file."""
    with open(file_path, 'w') as file:
        file.write("Artist Details:\n")
        file.write(f"Name: {artist_details['name']}\n")
        file.write(f"Genres: {', '.join(artist_details['genres'])}\n")
        file.write(f"Popularity: {artist_details['popularity']}\n")
        file.write(f"Followers: {artist_details['followers']['total']}\n\n")
        
        file.write("Albums:\n")
        for album in albums['items']:
            spotify_url = get_spotify_url(album)
            file.write(f" - {album['name']} ({album['release_date']}) - [Link]({spotify_url})\n")

file_path = f"{artist_details['name']}_Spotify_Data.txt"
export_to_txt(file_path, artist_details, albums)

print(f"Data exported to {file_path}")

# Export to Excel file}
def export_to_excel(file_path, artist_details, albums):
    """Export artist details and albums to an Excel file."""
    # Create a DataFrame for artist details
    artist_data = {
        'Name': [artist_details['name']],
        'Genres': [', '.join(artist_details['genres'])],
        'Popularity': [artist_details['popularity']],
        'Followers': [artist_details['followers']['total']]
    }
    artist_df = pd.DataFrame(artist_data)

    # Create a DataFrame for albums
    album_data = {
        'Name': [],
        'Release Date': [],
        'Spotify URL': []
    }
    for album in albums['items']:
        album_data['Name'].append(album['name'])
        album_data['Release Date'].append(album['release_date'])
        album_data['Spotify URL'].append(get_spotify_url(album))
    albums_df = pd.DataFrame(album_data)

    # Write data to Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        artist_df.to_excel(writer, sheet_name='Artist Details', index=False)
        albums_df.to_excel(writer, sheet_name='Albums', index=False)

file_path = f"{artist_details['name']}_Spotify_Data.xlsx"
export_to_excel(file_path, artist_details, albums)

print(f"Data exported to {file_path}")