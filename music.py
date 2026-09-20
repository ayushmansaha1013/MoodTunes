from ytmusicapi import YTMusic

ytmusic = YTMusic()  # No login/API key needed for search

def search_songs(query: str, limit=5):
    """Search YouTube Music and return a clean list of song dicts."""
    results = ytmusic.search(query, filter="songs", limit=limit)
    songs = []
    for r in results:
        songs.append({
            "title": r.get("title"),
            "artist": r["artists"][0]["name"] if r.get("artists") else "Unknown",
            "videoId": r.get("videoId"),
            "thumbnail": r["thumbnails"][-1]["url"] if r.get("thumbnails") else None,
        })
    return songs


# Quick test when run directly
if __name__ == "__main__":
    query = "upbeat pop hits"
    songs = search_songs(query)
    print(f"Results for: {query}\n")
    for s in songs:
        print(f"{s['title']} — {s['artist']}")
        print(f"  https://youtube.com/watch?v={s['videoId']}\n")