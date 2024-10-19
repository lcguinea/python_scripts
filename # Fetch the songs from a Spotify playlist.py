import requests
import pandas as pd
import os

# Token de acceso y ID de la lista de reproducción
spotify_access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')  # Asegúrate de configurar esta variable de entorno
spotify_playlist_id = '37i9dQZF1DXb0AsvHMF4aM'  # Cambia esto por la ID de tu lista de reproducción

def fetch_all_songs_from_playlist(playlist_id, access_token):
    spotify_headers = {'Authorization': f'Bearer {access_token}'}
    all_tracks = []
    offset = 0
    limit = 100  # Número máximo de canciones por solicitud

    while True:
        response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', 
                                headers=spotify_headers, 
                                params={'offset': offset, 'limit': limit})
        
        # Imprimir la respuesta para depuración
        print(f"Status code: {response.status_code}")
        response_json = response.json()
        print(f"Response JSON: {response_json}")

        if response.status_code == 200:
            if 'items' in response_json:
                tracks = response_json['items']
                all_tracks.extend(tracks)

                if len(tracks) < limit:
                    break  # Si hay menos canciones de las solicitadas, hemos llegado al final

                offset += limit
            else:
                print("La clave 'items' no está presente en la respuesta. Respuesta JSON completa:", response_json)
                break
        else:
            if 'error' in response_json:
                print(f"Error: {response_json['error']['message']}")
            else:
                print(f"Failed to fetch tracks. Status code: {response.status_code}")
            break

    return all_tracks

def create_playlist_table(tracks):
    # Lista para almacenar los datos de las canciones
    song_data = []
    for track in tracks:
        track_name = track['track']['name']
        artist_names = ', '.join(artist['name'] for artist in track['track']['artists'])
        song_data.append({'Track': track_name, 'Artists': artist_names})
    
    # Crear un DataFrame de pandas
    df = pd.DataFrame(song_data)
    return df

# Ejecutar la función
if spotify_access_token:
    tracks = fetch_all_songs_from_playlist(spotify_playlist_id, spotify_access_token)
    if tracks:
        df = create_playlist_table(tracks)
        print(df)  # Mostrar la tabla en la consola
        
        # Guardar la tabla en un archivo CSV
        csv_file_path = 'playlist_tracks.csv'
        df.to_csv(csv_file_path, index=False)  # index=False para no incluir los índices en el archivo CSV
        print(f"Datos guardados en '{csv_file_path}'")
else:
    print("Spotify access token not found. Please set the SPOTIFY_ACCESS_TOKEN environment variable.")