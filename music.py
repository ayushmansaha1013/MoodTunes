import requests

DEEZER_SEARCH_URL = "https://api.deezer.com/search"


def search_songs(query: str, limit=5):
    """
    Search for songs using Deezer's public API (free, no API key required).
    Returns 30-second preview URLs — reliable even from cloud servers.
    """
    params = {
        "q": query,
        "limit": limit,
    }

    try:
        response = requests.get(DEEZER_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"DEBUG Deezer API error: {e}")
        return []

    results = data.get("data", [])
    print(f"DEBUG: Deezer returned {len(results)} raw results")

    songs = []
    for item in results:
        songs.append({
            "title": item.get("title", "Unknown Title"),
            "artist": item.get("artist", {}).get("name", "Unknown Artist"),
            "videoId": None,
            "thumbnail": item.get("album", {}).get("cover_medium"),
            "previewUrl": item.get("preview"),  # 30-second MP3 preview, direct link
            "trackViewUrl": item.get("link"),   # link to open on Deezer
        })

    return songs


if __name__ == "__main__":
    query = "upbeat pop hits"
    songs = search_songs(query)
    print(f"Results for: {query}\n")
    for s in songs:
        print(f"{s['title']} — {s['artist']}")
        print(f"  Preview: {s['previewUrl']}")
        print(f"  Link: {s['trackViewUrl']}\n")
    for s in songs:
        print(f"{s['title']} — {s['artist']}")
        print(f"  Preview: {s['previewUrl']}")
        print(f"  Link: {s['trackViewUrl']}\n")
