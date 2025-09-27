import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re

def main():
    # Set up authentication
    
    # Function to fetch tracks from a playlist
    def fetch_playlist_tracks(playlist_id):
        results = sp.playlist_items(playlist_id)
        tracks = []
        for item in results['items']:
            track = item['track']
            tracks.append({
                'Name': track['name'],
                'Artist': ', '.join([artist['name'] for artist in track['artists']]),
                'Album': track['album']['name'],
                'Release Date': track['album']['release_date'],
                'Duration (ms)': track['duration_ms']
            })
        return tracks

    # Example: Fetch tracks from a playlist
    playlist_id = "your_playlist_id"
    tracks = fetch_playlist_tracks(playlist_id)

    # Save to a CSV
    df = pd.DataFrame(tracks)
    df.to_csv('playlist_tracks.csv', index=False)
    print("Tracks saved to playlist_tracks.csv")

def conn():
    # Set up authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="7ea69b825c1b45ee8ea81388ea2e4ce6",
        client_secret="562448edd53b4b779c8edf6506575fc9",
        redirect_uri="http://localhost:3000",
        scope="user-read-private"
    ))

    # Fetch and display your profile info
    profile = sp.me()
    print("Display Name:", profile['display_name'])
    print("User ID:", profile['id'])
    print("Email:", profile.get('email', 'No email associated'))


def get_playlist_ids():
    links = [
        "https://open.spotify.com/playlist/1ZmDYSCQTdE556cMWAJmF3?si=0885719b85bd4ef7"
    ]
    ids = []
    for link in links:
        playlist_id = re.search(r'playlist/([^/?]+)', link).group(1)
        ids.append(playlist_id)
    print(ids)


if __name__ == '__main__':
    # main()

    conn()
    get_playlist_ids()










































