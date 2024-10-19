# Look for a song in YouTube

from googleapiclient.discovery import build

# Configura tu clave de API de YouTube
youtube_api_key = 'AIzaSyDQyLR4s76KwpOYlKYJupo-ccuy8FMd9po'

# Función para buscar canciones en YouTube
def search_youtube(query, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

# Ejemplo de búsqueda
query = "Shape of You Ed Sheeran"
youtube_url = search_youtube(query, youtube_api_key)
print(youtube_url)
