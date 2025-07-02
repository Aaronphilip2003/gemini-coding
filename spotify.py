import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_playlist_names():
    """
    Connects to the Spotify API and fetches the current user's playlist names.

    Requires the following environment variables to be set in a .env file:
    - SPOTIPY_CLIENT_ID: Your Spotify application's client ID.
    - SPOTIPY_CLIENT_SECRET: Your Spotify application's client secret.
    - SPOTIPY_REDIRECT_URI: The redirect URI configured in your Spotify app.
    """
    # Check for environment variables
    if not all(k in os.environ for k in ["SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI"]):
        print("Error: Make sure you have set the SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI environment variables in your .env file.")
        return

    # Set up authentication
    scope = "playlist-read-private"
    auth_manager = SpotifyOAuth(scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get the current user's username
    try:
        user = sp.current_user()
        username = user['id']
    except Exception as e:
        print(f"Error getting user info: {e}")
        print("Could not authenticate. Please check your credentials and try again.")
        return

    print(f"Authenticated as {user['display_name']} ({username}). Fetching playlists...")

    # Get playlists
    playlists = []
    results = sp.current_user_playlists(limit=50)
    
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    if not playlists:
        print("You don't have any playlists yet.")
        return

    # Print playlist names
    print("\nYour Spotify Playlists:")
    for i, playlist in enumerate(playlists):
        print(f"{i + 1}. {playlist['name']}")

if __name__ == "__main__":
    get_playlist_names()
