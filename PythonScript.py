import requests
import pandas as pd

#Your Spotify API credentials
CLIENT_ID = '32ff63d08e0c49528cda7c12df684119'
CLIENT_SECRET = '3ced7f52cdc749afb16250f30d136993'

# Function to get Spotify API token
def get_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Function to search for a track and get the album cover URL
def get_album_cover_url(token, track_name, artist_name):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'q': f'track:{track_name} artist:{artist_name}',
        'type': 'track',
        'limit': 1,
    }
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    if data['tracks']['items']:
        album = data['tracks']['items'][0]['album']
        return album['images'][0]['url']  # URL of the largest image
    return None

# Load your dataset
df = pd.read_csv('spotify-2023.csv',encoding='ISO-8859-1')

# Get Spotify API token
token = get_token(CLIENT_ID, CLIENT_SECRET)

# Add a new column for album cover URLs
df['album_cover_url'] = df.apply(
    lambda row: get_album_cover_url(token, row['track_name'], row['artist_name']),
    axis=1
)

# Save the updated dataset
df.to_csv('updated_dataset.csv', index=False)
