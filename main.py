import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

PLAYLIST_SCOPE = "playlist-modify-public"
songs = []

def get_songs():
    url = "https://www.billboard.com/charts/hot-100/"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

    chosen_day = input("Which day do you choose? Type the date in the format YYYY-MM-DD.\n")

    response = requests.get(f"{url}/{chosen_day}/", headers=header)

    soup = BeautifulSoup(response.text, "html.parser")

    all_songs_info = soup.find_all(name="div", class_="o-chart-results-list-row-container")

    for song_tag in all_songs_info:
        li = song_tag.find(name="li", class_="lrv-u-width-100p")
        s = li.find(name="h3")
        a = li.find(name="span")
        songs.append(f"{s.text.strip()} {a.text.strip()}")

    return chosen_day

def create_playlist():
    auth_manager = SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                client_secret=os.environ["CLIENT_SECRET"],
                                redirect_uri="http://example.com",
                                scope=PLAYLIST_SCOPE)
    sp = spotipy.Spotify(
        auth_manager=auth_manager
    )

    result = sp.user_playlist_create(
        user=os.environ["USER_ID"],
        name=f"HOT 100 in {day}",
        public=True,
        collaborative=False,
        description=f"These are the HOT 100 songs in {day}",
    )

    return result["external_urls"]["spotify"]


def search_song(song_name):
    auth_manager = SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                client_secret=os.environ["CLIENT_SECRET"],
                                redirect_uri="http://example.com",
                                scope=PLAYLIST_SCOPE)
    sp = spotipy.Spotify(
        auth_manager=auth_manager
    )
    result = sp.search(
        q=song_name,
        limit=1,
        type="track",
    )
    return result["tracks"]["items"][0]["external_urls"]["spotify"]


def add_songs():
    auth_manager = SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                client_secret=os.environ["CLIENT_SECRET"],
                                redirect_uri="http://example.com",
                                scope=PLAYLIST_SCOPE)
    sp = spotipy.Spotify(
        auth_manager=auth_manager
    )
    sp.playlist_add_items(
        playlist_id=playlist_url,
        items=songs_urls,
    )


day = get_songs()
playlist_url = create_playlist()

songs_urls = []
print("Searching songs...")
for song in songs:
    song_url = search_song(song).strip()
    songs_urls.append(song_url)

print("Adding songs...")
add_songs()