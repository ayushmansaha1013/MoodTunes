import streamlit as st
import cv2
import numpy as np
from PIL import Image
from deepface import DeepFace

from mood_map import get_query_for_emotion, get_explanation_for_emotion
from music import search_songs

MOOD_COLORS = {
    'happy':    "#FFD93D",
    'sad':      "#4A90D9",
    'angry':    "#E63946",
    'fear':     "#6C5CE7",
    'surprise': "#FF9F43",
    'neutral':  "#95A5A6",
    'disgust':  "#2ECC71",
}

st.set_page_config(page_title="MoodTunes", page_icon="🎵", layout="centered")

st.title("🎵 MoodTunes")
st.write("AI-powered music recommendations based on your facial emotion.")

# ---------------- Session state init ----------------
if "history" not in st.session_state:
    st.session_state.history = []
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "captures" not in st.session_state:
    st.session_state.captures = []
if "expanded_song" not in st.session_state:
    st.session_state.expanded_song = None
if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = None
if "current_query" not in st.session_state:
    st.session_state.current_query = None

# ---------------- Camera + multi-capture smoothing ----------------
st.write("For best accuracy, capture up to 3 photos — we'll average the results to reduce noise.")

img_file = st.camera_input("Take a photo to detect your mood")

col1, col2 = st.columns(2)
with col1:
    if img_file is not None and st.button("➕ Add this capture"):
        image = Image.open(img_file)
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

            if len(result) > 1:
                st.warning(
                    f"⚠️ {len(result)} faces detected in this photo. "
                    f"Using the largest/most prominent face for mood detection."
                )
                result = sorted(
                    result,
                    key=lambda r: r['region']['w'] * r['region']['h'],
                    reverse=True
                )

            st.session_state.captures.append(result[0]['emotion'])
            st.success(f"Capture {len(st.session_state.captures)} added.")
        except Exception:
            st.error("Couldn't detect a face in this photo. Try again or use manual selection below.")
with col2:
    if st.button("🔄 Reset captures"):
        st.session_state.captures = []
        st.rerun()

st.caption(f"Captures collected: {len(st.session_state.captures)} / 3 recommended")

detected_emotion = None
confidence = None
avg_scores = None

if st.session_state.captures:
    all_emotions = st.session_state.captures[0].keys()
    avg_scores = {
        emo: sum(c[emo] for c in st.session_state.captures) / len(st.session_state.captures)
        for emo in all_emotions
    }
    detected_emotion = max(avg_scores, key=avg_scores.get)
    confidence = avg_scores[detected_emotion]
    st.success(f"Detected emotion (averaged over {len(st.session_state.captures)} capture(s)): "
               f"**{detected_emotion.upper()}** ({confidence:.1f}% confidence)")

    st.write("**Emotion breakdown:**")
    st.bar_chart(avg_scores)

# ---------------- Manual override ----------------
st.divider()
st.write("**Or select your mood manually:**")

manual_emotion = st.selectbox(
    "Choose a mood",
    ["-- None --", "happy", "sad", "angry", "fear", "surprise", "neutral", "disgust"]
)

final_emotion = None
if manual_emotion != "-- None --":
    final_emotion = manual_emotion
elif detected_emotion:
    final_emotion = detected_emotion

# ---------------- Recommendations ----------------
if final_emotion:
    accent = MOOD_COLORS.get(final_emotion, "#6C5CE7")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {accent}33;
        }}
        div.stButton > button {{
            background-color: {accent};
            color: white;
            border: none;
        }}
        div.stButton > button:hover {{
            background-color: {accent}CC;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Only pick a new random query when the emotion actually changes.
    # This prevents the song list from shuffling on every rerun
    # (e.g. when clicking "Bookmark"), which was breaking playback + bookmarking.
    if st.session_state.current_emotion != final_emotion:
        st.session_state.current_emotion = final_emotion
        st.session_state.current_query = get_query_for_emotion(final_emotion)

    query = st.session_state.current_query
    st.caption(f"Mood: **{final_emotion}** → Searching for: *{query}*")

    with st.spinner("Finding songs for your mood..."):
        songs = search_songs(query, limit=5)[:5]

    if not st.session_state.history or st.session_state.history[-1]["emotion"] != final_emotion:
        st.session_state.history.append({"emotion": final_emotion, "songs": songs})

    st.subheader("🎧 Recommended for you")

    for song in songs:
        is_open = st.session_state.expanded_song == song["videoId"]
        with st.expander(f"🎵 {song['title']} — {song['artist']}", expanded=is_open):
            st.caption(f"💡 {get_explanation_for_emotion(final_emotion)}")
            if song["videoId"]:
                st.video(f"https://youtube.com/watch?v={song['videoId']}")

            already_bookmarked = any(
                b["videoId"] == song["videoId"] for b in st.session_state.bookmarks
            )
            if already_bookmarked:
                st.caption("❤️ Bookmarked")
            else:
                if st.button("🤍 Bookmark this song", key=f"bookmark_{song['videoId']}"):
                    st.session_state.bookmarks.append(song)
                    st.session_state.expanded_song = song["videoId"]

# ---------------- Sidebar: History + Bookmarks ----------------
with st.sidebar:
    st.header("📜 Mood History")
    if st.session_state.history:
        for entry in reversed(st.session_state.history):
            st.write(f"**{entry['emotion'].capitalize()}** — {len(entry['songs'])} songs")

        if len(st.session_state.history) >= 2:
            st.write("**Mood trend this session:**")
            valence_map = {
                'happy': 6, 'surprise': 5, 'neutral': 4,
                'fear': 3, 'disgust': 2, 'sad': 1, 'angry': 0
            }
            trend_values = [valence_map.get(e['emotion'], 3) for e in st.session_state.history]
            st.line_chart(trend_values)
    else:
        st.caption("No moods detected yet this session.")

    st.divider()

    st.header("❤️ Bookmarked Songs")
    if st.session_state.bookmarks:
        for song in st.session_state.bookmarks:
            st.write(f"**{song['title']}**")
            st.write(song['artist'])
            st.markdown(f"[▶️ Play](https://youtube.com/watch?v={song['videoId']})")
            st.divider()
    else:
        st.caption("No bookmarks yet. Click 🤍 on a song to save it.")