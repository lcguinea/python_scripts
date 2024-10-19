# %%
import requests

# Replace with your actual refresh token
REFRESH_TOKEN = 'lZlhKk3G6jmJLK2GsAfbGfYMwFNryqretb4ip7n9I22kH1c6trhtgGHNAZqzVJRT'
ARTIST_NAME = 'Taylor Swift'  # Replace with the actual artist name

def get_access_token(refresh_token):
    auth_url = 'https://api.chartmetric.com/api/token'
    payload = {'refreshtoken': refresh_token}
    response = requests.post(auth_url, json=payload)
    if response.status_code == 200:
        access_token = response.json().get('token')
        return access_token
    else:
        raise Exception(f'Failed to authenticate: {response.status_code}, {response.text}')

def search_artist_by_name(access_token, artist_name):
    url = f'https://api.chartmetric.com/api/search?type=artists&q={artist_name}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        search_results = response.json()
        if search_results['obj']['artists']:
            artist_id = search_results['obj']['artists'][0]['id']
            return artist_id
        else:
            raise Exception('Artist not found')
    else:
        raise Exception(f'Failed to search artist: {response.status_code}, {response.text}')

def fetch_artist_details(access_token, artist_id):
    url = f'https://api.chartmetric.com/api/artist/{artist_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to fetch artist details: {response.status_code}, {response.text}')

def main():
    try:
        access_token = get_access_token(REFRESH_TOKEN)
        artist_id = search_artist_by_name(access_token, ARTIST_NAME)
        artist_details = fetch_artist_details(access_token, artist_id)
        artist_image_url = artist_details['obj'].get('image_url', '')
        print(f"Artist Image URL: {artist_image_url}")
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()


