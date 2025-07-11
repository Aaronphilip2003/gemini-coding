import os
import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_songs_from_playlist(playlist_name):
    """
    Connects to the Spotify API and fetches all songs from a specific playlist.

    Requires environment variables for Spotify authentication.
    """
    # Set up authentication
    scope = "playlist-read-private"
    try:
        auth_manager = SpotifyOAuth(scope=scope)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        user = sp.current_user()
        print(f"Authenticated as {user['display_name']} ({user['id']}).")
    except Exception as e:
        print(f"Error during authentication: {e}")
        print("Could not authenticate. Please check your credentials and try again.")
        return

    # Find the target playlist
    print(f"Searching for playlist: '{playlist_name}'...")
    playlists = []
    results = sp.current_user_playlists(limit=50)
    playlists.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])

    target_playlist = None
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            target_playlist = playlist
            break

    if not target_playlist:
        print(f"Error: Playlist '{playlist_name}' not found.")
        return

    print(f"Found playlist! ID: {target_playlist['id']}")
    print("\nFetching songs from '{playlist_name}'...")

    # Get all tracks from the playlist
    tracks = []
    results = sp.playlist_items(target_playlist['id'], fields='items(track(name, artists(name))),next')
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    if not tracks:
        print("No songs found in this playlist.")
        return

    # Save songs to a CSV file
    csv_file_name = f"{playlist_name}.csv"
    try:
        with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Song Name', 'Artist Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in tracks:
                track = item.get('track')
                if track:
                    song_name = track['name']
                    artist_name = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
                    writer.writerow({'Song Name': song_name, 'Artist Name': artist_name})
        print(f"\nSuccessfully saved songs to '{csv_file_name}'.")
    except IOError as e:
        print(f"\nError writing to CSV file: {e}")


if __name__ == "__main__":
    # Name of the playlist you want to get songs from
    target_playlist_name = "LikedSongsPlayList2025"
    get_songs_from_playlist(target_playlist_name)
