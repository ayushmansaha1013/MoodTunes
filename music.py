import requests

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


def search_songs(query: str, limit=5):
    """
    Search for songs using Apple's iTunes Search API (free, no API key required,
    and works reliably from cloud servers unlike YouTube-based scraping APIs).

    Returns a list of dicts with the same shape the app expects:
    { "title": ..., "artist": ..., "videoId": ..., "thumbnail": ..., "previewUrl": ... }
    """
    params = {
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": limit,
    }

    try:
        response = requests.get(ITUNES_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    songs = []
    for item in data.get("results", []):
        songs.append({
            "title": item.get("trackName", "Unknown Title"),
            "artist": item.get("artistName", "Unknown Artist"),
            "videoId": None,  # no longer using YouTube video IDs
            "thumbnail": item.get("artworkUrl100"),
            "previewUrl": item.get("previewUrl"),  # 30-second audio preview
            "trackViewUrl": item.get("trackViewUrl"),  # link to open in Apple Music/iTunes
        })

    return songs


# Quick test when run directly
if __name__ == "__main__":
    query = "upbeat pop hits"
    songs = search_songs(query)
    print(f"Results for: {query}\n")
    for s in songs:
        print(f"{s['title']} — {s['artist']}")
        print(f"  Preview: {s['previewUrl']}")
        print(f"  Link: {s['trackViewUrl']}\n")
