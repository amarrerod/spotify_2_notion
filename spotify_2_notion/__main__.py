import spotipy
from dotenv import dotenv_values
from notion_client import Client
from spotipy.oauth2 import SpotifyClientCredentials

from .models import Track

if __name__ == "__main__":
    config = dotenv_values(".env")
    notion = Client(auth=config["NOTION_TOKEN"])
    my_page = notion.databases.query(**{"database_id": config["NOTION_DATABASE_ID"]})

    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=config["SPOTIPY_CLIENT_ID"],
            client_secret=config["SPOTIPY_CLIENT_SECRET"],
        )
    )
    results = spotify.playlist_tracks(config["SPOTIPY_PLAYLIST_ID"])
    items = list(dict(**item["track"]) for item in results["items"])

    for item in items:
        features = dict(**spotify.audio_features(item["id"])[0])
        t = Track.from_query(item, features)
        notion.pages.create(
            parent={"database_id": config["NOTION_DATABASE_ID"]}, properties=t.to_page()
        )
        print(f"Added: {t.title}")
