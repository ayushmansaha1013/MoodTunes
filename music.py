import requests
from urllib.parse import quote_plus

DEEZER_SEARCH_URL = "https://api.deezer.com/search"


def search_songs(query: str, limit=5):
    params = {
        "q": query,
        "limit": limit,
    }

    try:
        response = requests.get(
            DEEZER_SEARCH_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Deezer API error: {e}")
        return []

    songs = []

    for item in data.get("data", []):
        title = item.get("title", "Unknown Title")
        artist = item.get("artist", {}).get("name", "Unknown Artist")

        youtube_query = quote_plus(f"{title} {artist} official")

        songs.append({
            "title": title,
            "artist": artist,
            "thumbnail": item.get("album", {}).get("cover_medium"),
            "previewUrl": item.get("preview"),
            "deezerUrl": item.get("link"),
            "youtubeUrl": f"https://www.youtube.com/results?search_query={youtube_query}",
        })

    return songs
