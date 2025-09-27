import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re
import time
from collections import Counter


def get_track_genre_from_artist(track_details):
    # Get artist IDs from the track
    artist_ids = [artist['id'] for artist in track_details['artists']]
    all_genres = []
    for artist_id in artist_ids:
        artist_data = sp.artist(artist_id)
        all_genres.extend(artist_data['genres'])
    return str(all_genres)


# Function to fetch tracks from a playlist
def fetch_playlist_tracks(sp, playlist_id):
    playlist = sp.playlist(playlist_id)
    playlist_name = playlist['name']
    print(f"pulling songs from the playlist: '{playlist_name}'")
    all_tracks = []
    track_data = []
    offset = 0
    limit = 100
    while True:
        chuck_tracks = sp.playlist_items(playlist_id, offset=offset, limit=limit)['items']
        if not chuck_tracks:
            break
        all_tracks.extend(chuck_tracks)
        offset += limit

    for track in all_tracks:
        track_details = track['track']
        # genres = get_track_genre_from_artist(track_details)
        genres = 'test genre'
        track_data.append({
            "playlist_name": playlist_name,
            "explicit": track_details["explicit"],
            "type": track_details["type"],
            "episode": track_details["episode"],
            "track": track_details["track"],
            "album_type": track_details['album']['type'],
            "album_album": track_details['album']['album_type'],
            "album_href": track_details['album']['href'],
            "album_id": track_details['album']['id'],
            "album_name": track_details['album']['name'],
            "album_release": track_details['album']['release_date'],
            "album_release": track_details['album']['release_date_precision'],
            "album_uri": track_details['album']['uri'],
            "artist_id": track_details['artists'][0]['id'],
            "artist_name": track_details['artists'][0]['name'],
            "artist_type": track_details['artists'][0]['type'],
            "artist_uri": track_details['artists'][0]['uri'],
            "disc_number": track_details['disc_number'],
            "track_number": track_details['track_number'],
            "duration_ms": track_details['duration_ms'],
            "id": track_details['id'],
            "name": track_details['name'],
            "popularity": track_details['popularity'],
            "uri": track_details['uri'],
            "is_local": track_details['is_local'],
            "all_spotify_genres": genres
        })

    # Convert dictionaries to tuples (hashable)
    hashable_list = [tuple(sorted(d.items())) for d in track_data]

    # Count occurrences of each item
    counts = Counter(hashable_list)

    # Identify problematic items
    problematic_items = [dict(item) | {"count_in_playlist": count} for item, count in counts.items() if count != 2]

    # Deduplicate (only items appearing exactly twice)
    deduplicated_list = [dict(item) | {"count_in_playlist": count} for item, count in counts.items() if count == 2]

    if problematic_items:
        print("All songs are expected to appear on a playlist twice.\n"
              f"Playlist: '{playlist_name}' has {len(problematic_items)} items with unexpected counts:")
        for problematic_item in problematic_items:
            bad_name = problematic_item['name']
            artist_name = problematic_item['artist_name']
            bad_count = problematic_item['count_in_playlist']
            print(f"   {bad_name} by {artist_name} appears {bad_count} times(s). It was added to the data anyway")
            deduplicated_list.append(problematic_item)

    return deduplicated_list


def main(sp, playlist_ids):
    tracks = []
    chunk_size = 5
    for i, playlist in enumerate(playlist_ids):
        new_track = fetch_playlist_tracks(sp, playlist)
        # print(new_track[0].keys())
        tracks += new_track

        # idk what this is or if I need it
        # for i, item in enumerate(tracks):
        #     if not isinstance(item, dict):
        #         print(f"Item at index {i} is not a dictionary: {item}")
        # Save to a CSV
        if i % chunk_size == 0:
            df = pd.DataFrame(tracks)
            df.to_csv(f"playlist_tracks_{i}.csv", index=False)
            print(f"Tracks saved to playlist_tracks{i}.csv")
            tracks = []


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
    # print("Display Name:", profile['display_name'])
    # print("User ID:", profile['id'])
    # print("Email:", profile.get('email', 'No email associated'))
    print(f"Connected to {profile['display_name']} Spotify Profile")
    return sp


def get_playlist_ids():
    links = [
        "https://open.spotify.com/playlist/1ZmDYSCQTdE556cMWAJmF3?si=0885719b85bd4ef7",
        "https://open.spotify.com/playlist/1IOW3J6G1iARCUaIjoRG3T?si=8158bce9a551463d",
        "https://open.spotify.com/playlist/4IVfLI83ynMpQydzxVVQyR?si=a1e22c061f584be4",
        "https://open.spotify.com/playlist/7HMJn8fg3ZGdpVuxPfQMWC?si=29122d2ccc75458f",
        "https://open.spotify.com/playlist/5CoVHxsWGjM2pRPYxwMICc?si=3e018a5a28a84ded",
        "https://open.spotify.com/playlist/6fj1WZEyI2PW2LdHk02pYJ?si=5965632b651a4c46",
        "https://open.spotify.com/playlist/3zQxDZWokhWNnYgfj2pCER?si=6a5d968df4504eb1",
        "https://open.spotify.com/playlist/7BuZbE8ZY4qgqsPphsQ1Ad?si=cac9f12a99e74eda",
        "https://open.spotify.com/playlist/4YsoIPiFeTfaPRqf96kC6b?si=8fe282ce30d54895",
        "https://open.spotify.com/playlist/4ExyGMZRnH5m3kRPP5BF2k?si=daeb2a5e30874d6c",
        "https://open.spotify.com/playlist/32rKQzyfWWaOzKy3Z7iwty?si=d4c0284dabbd43a5",
        "https://open.spotify.com/playlist/2PLbiKEvT6fSqUvq6bu5mw?si=88873de816ac46a7",
        "https://open.spotify.com/playlist/4yvBO0UDLH8ZkiXLxjSmAh?si=651716b919114e1f",
        "https://open.spotify.com/playlist/3RcCidDEfr8Shwv2OPKPlp?si=9360cd49344d4119",
        "https://open.spotify.com/playlist/5Nbwj7fEdjPHsdr8N63npq?si=14a737ddda9341de",
        "https://open.spotify.com/playlist/3KYkVopWFlrkceHQqRUtfT?si=162800445cf34e56",
        "https://open.spotify.com/playlist/0TYGNavqTSZtRopbrE8BA2?si=e9f6a91a113a4438",
        "https://open.spotify.com/playlist/0p2Z4iBSs6S4PSSlDgRRkB?si=49dc07fb3e7f4bf5",
        "https://open.spotify.com/playlist/27LcdAuYmfJpTBJi04XGno?si=a4bab396bd084214",
        "https://open.spotify.com/playlist/542e9cESmee2iGqSNKCPak?si=aee03a482df2480c",
        "https://open.spotify.com/playlist/6pPVjd0Bcfoef3gYCRhvEM?si=84674e7ecce6433d",
        "https://open.spotify.com/playlist/7JZs7DS24KDqKAGU8KWuZD?si=e2ae02ae27f84006",
        "https://open.spotify.com/playlist/0HbAjC6AhHlQbW7r57mPKw?si=d2d197ba11e84ab3",
        "https://open.spotify.com/playlist/6nvEphcessFCK0KKdRojjN?si=334f67030df64005",
        "https://open.spotify.com/playlist/6zCaOBnecUUQNOLpkW4m1H?si=b879ed630f324b04",
        "https://open.spotify.com/playlist/4YzqzwzvRFs2RJtnP5WTeU?si=3195ec2f07c34ee3",
        "https://open.spotify.com/playlist/0FuaeloXPXSkDA2CUaXzKy?si=bc5ac0c5323d4dcc",
        "https://open.spotify.com/playlist/2DFyeDKMjHUoAx0qfDEf3y?si=e30d5fd7d08d4c89",
        "https://open.spotify.com/playlist/03VXb8rubrUPW7zQmkPdua?si=fac17e87295a4880",
        "https://open.spotify.com/playlist/0ozfWMGBUfUSSkNdVosF4z?si=54e412e2e74747c1",
        "https://open.spotify.com/playlist/4jnaFGoOpuGMAKP4nCzXeS?si=cf6657f6a529472c",
        "https://open.spotify.com/playlist/5ST52UmaNyvjYOVtcczs71?si=69ca103fd42d4265",
        "https://open.spotify.com/playlist/22fXr46I7QvIOhXpwtxdVw?si=69e5e0620bd942d8",
        "https://open.spotify.com/playlist/6Sowqio01x7aTwaGSiWxKZ?si=c1a339ec41824021",
        "https://open.spotify.com/playlist/3vincZSJQm2MNV72YGarQa?si=387fa8153c0c461b",
        "https://open.spotify.com/playlist/32xA2cF6koaEuPKbfDSi3K?si=f67ba6ba9e1f48c0",
        "https://open.spotify.com/playlist/5QJf2Xos833n4BDgmOlhjv?si=de0bec62f1ff4889",
        "https://open.spotify.com/playlist/0DMeklyNO3JwvXcAKlGGtP?si=82bc759b151c41fa",
        "https://open.spotify.com/playlist/6ZmfFgPf6riV6BE9E0kWno?si=fb3857b5c5634e65",
        "https://open.spotify.com/playlist/4WBmvsASPnFv5Xpxbh6h3P?si=bab5ffb9ae974a73",
        "https://open.spotify.com/playlist/4aURj4qsNGehWVTMxoS89z?si=c3e4dd4f07b0454d",
        "https://open.spotify.com/playlist/29bFeBXx0qBrxHCBSkuCN0?si=f8408a59d53d4cce",
        "https://open.spotify.com/playlist/2MWtTaGfoBnBwRR7z73wzN?si=7234f0e8120e4cad",
        "https://open.spotify.com/playlist/1bny6qpgk8sJwrT3RUFvdF?si=9d093990028e40ae",
        "https://open.spotify.com/playlist/6TCyjm2GzUbRkkbf3a3atY?si=e3393a714c40481d",
        "https://open.spotify.com/playlist/0w2zZXiZG6EWV1BiwdXodd?si=e176cbaa8b824078",
        "https://open.spotify.com/playlist/7cYJDBPgYJne2MOAkdFk1Z?si=a189420e07e8411c",
        "https://open.spotify.com/playlist/6eW7qbdWxMyU7OilIXNVAR?si=8e15fc0adc374770",
        "https://open.spotify.com/playlist/7zHoMdcqPE0biLYM6lBjuc?si=b164dced43fe4099",
        "https://open.spotify.com/playlist/79fEaOigXi2jzERRHbAskQ?si=6c4d69d7a447437e",
        "https://open.spotify.com/playlist/1i0QkSCOm2qsDTtB6DzSa6?si=221d7fa8765c47c4",
        "https://open.spotify.com/playlist/7rbcdgz1dwrqzhBsPgzLW5?si=64477bccf7d64196",
        "https://open.spotify.com/playlist/09MrmHGtnpZJlusg35dAcw?si=f31ffd426efd4acb",
        "https://open.spotify.com/playlist/0fPnUKczjfRAvDrAjABvuH?si=014e6ad3220d49e3",
        "https://open.spotify.com/playlist/722fDu1dk7wwhV3z3AuX5F?si=d470a91e3c484c28",
        "https://open.spotify.com/playlist/5CQblPuDQwQZLn9uCOi6gZ?si=c4b0165771094073"
    ]
    ids = []
    for link in links:
        playlist_id = re.search(r'playlist/([^/?]+)', link).group(1)
        ids.append(playlist_id)
    # print(ids)
    return ids


if __name__ == '__main__':
    # main()

    sp = conn()
    playlist_ids = get_playlist_ids()
    main(sp, playlist_ids)










































