import os

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from deepface import DeepFace

from mood_map import get_query_for_emotion, get_explanation_for_emotion
from music import search_songs


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MoodTunes",
    page_icon="🎵",
    layout="centered"
)


# ============================================================
# CACHED MUSIC SEARCH
# ============================================================

@st.cache_data(ttl=300)
def get_songs(query):
    return search_songs(query, limit=5)


# ============================================================
# MOOD COLORS
# ============================================================

MOOD_COLORS = {
    "happy": "#FFD93D",
    "sad": "#4A90D9",
    "angry": "#E63946",
    "fear": "#6C5CE7",
    "surprise": "#FF9F43",
    "neutral": "#95A5A6",
    "disgust": "#2ECC71",
}


# ============================================================
# HEADER
# ============================================================

st.title("🎵 MoodTunes")
st.write("AI-powered music recommendations based on your facial emotion.")


# ============================================================
# SESSION STATE
# ============================================================

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


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📜 Mood History")

    if st.session_state.history:

        for entry in reversed(st.session_state.history):

            st.write(
                f"**{entry['emotion'].capitalize()}** "
                f"— {len(entry['songs'])} songs"
            )

        if len(st.session_state.history) >= 2:

            st.write("**Mood trend this session:**")

            valence_map = {
                "happy": 6,
                "surprise": 5,
                "neutral": 4,
                "fear": 3,
                "disgust": 2,
                "sad": 1,
                "angry": 0,
            }

            trend_values = [
                valence_map.get(
                    entry["emotion"],
                    3
                )
                for entry in st.session_state.history
            ]

            st.line_chart(trend_values)

    else:

        st.caption("No moods detected yet this session.")

    st.divider()

    st.header("❤️ Bookmarked Songs")

    if st.session_state.bookmarks:

        for song in st.session_state.bookmarks:

            st.write(f"**{song['title']}**")
            st.write(song["artist"])

            if song.get("previewUrl"):

                st.audio(song["previewUrl"])

            if song.get("youtubeUrl"):

                st.link_button(
                    "▶️ Watch on YouTube",
                    song["youtubeUrl"]
                )

            st.divider()

    else:

        st.caption(
            "No bookmarks yet. "
            "Click 🤍 on a song to save it."
        )

    # --------------------------------------------------------
    # OpenCV diagnostic
    # --------------------------------------------------------

    with st.expander("🔧 System diagnostics"):

        st.write(
            f"OpenCV version: `{cv2.__version__}`"
        )

        cascade_dir = cv2.data.haarcascades

        cascade_file = os.path.join(
            cascade_dir,
            "haarcascade_frontalface_default.xml"
        )

        st.write(
            f"Cascade directory: `{cascade_dir}`"
        )

        cascade_exists = os.path.exists(cascade_file)

        if cascade_exists:
            st.success(
                "✅ OpenCV Haar cascade found."
            )
        else:
            st.error(
                "❌ OpenCV Haar cascade is missing."
            )

        st.caption(
            "The diagnostic is useful if DeepFace emotion "
            "detection fails on deployment."
        )


# ============================================================
# CAMERA / FACE DETECTION
# ============================================================

st.subheader("📷 Detect Your Mood")

st.write(
    "For best accuracy, capture up to 3 photos. "
    "MoodTunes averages the results to reduce noise."
)

img_file = st.camera_input(
    "Take a photo to detect your mood"
)


col1, col2 = st.columns(2)


# ============================================================
# ADD CAPTURE
# ============================================================

with col1:

    if img_file is not None:

        if st.button("➕ Add this capture"):

            image = Image.open(img_file)

            frame = cv2.cvtColor(
                np.array(image),
                cv2.COLOR_RGB2BGR
            )

            try:

                # ------------------------------------------------
                # DeepFace emotion analysis
                # ------------------------------------------------

                result = DeepFace.analyze(
                    img_path=frame,
                    actions=["emotion"],
                    enforce_detection=False,
                    detector_backend="opencv"
                )

                # DeepFace versions may return a dict or list
                if isinstance(result, dict):
                    result = [result]

                if not result:

                    raise ValueError(
                        "DeepFace returned no analysis result."
                    )

                # ------------------------------------------------
                # If multiple faces are detected,
                # choose the largest face.
                # ------------------------------------------------

                if len(result) > 1:

                    st.warning(
                        f"⚠️ {len(result)} faces detected. "
                        "Using the largest face."
                    )

                    result = sorted(
                        result,
                        key=lambda r:
                        r["region"]["w"] *
                        r["region"]["h"],
                        reverse=True
                    )

                emotion_scores = result[0]["emotion"]

                st.session_state.captures.append(
                    emotion_scores
                )

                st.success(
                    f"✅ Capture "
                    f"{len(st.session_state.captures)} added."
                )

            except Exception as e:

                st.error(
                    "❌ Emotion detection failed."
                )

                st.exception(e)


# ============================================================
# RESET CAPTURES
# ============================================================

with col2:

    if st.button("🔄 Reset captures"):

        st.session_state.captures = []

        st.session_state.current_emotion = None
        st.session_state.current_query = None

        st.rerun()


# ============================================================
# CAPTURE COUNT
# ============================================================

st.caption(
    f"Captures collected: "
    f"{len(st.session_state.captures)} / 3 recommended"
)


# ============================================================
# EMOTION CALCULATION
# ============================================================

detected_emotion = None
confidence = None
avg_scores = None


if st.session_state.captures:

    all_emotions = st.session_state.captures[0].keys()

    avg_scores = {
        emotion: sum(
            capture[emotion]
            for capture in st.session_state.captures
        ) / len(st.session_state.captures)

        for emotion in all_emotions
    }

    detected_emotion = max(
        avg_scores,
        key=avg_scores.get
    )

    confidence = avg_scores[
        detected_emotion
    ]

    st.success(
        f"😊 Detected emotion "
        f"(averaged over "
        f"{len(st.session_state.captures)} capture(s)): "
        f"**{detected_emotion.upper()}** "
        f"({confidence:.1f}% confidence)"
    )

    st.write("**Emotion breakdown:**")

    st.bar_chart(avg_scores)


# ============================================================
# MANUAL MOOD OVERRIDE
# ============================================================

st.divider()

st.subheader("🎛️ Choose Your Mood")

st.write(
    "You can also select a mood manually."
)

manual_emotion = st.selectbox(
    "Choose a mood",
    [
        "-- None --",
        "happy",
        "sad",
        "angry",
        "fear",
        "surprise",
        "neutral",
        "disgust",
    ]
)


# ============================================================
# FINAL EMOTION
# ============================================================

final_emotion = None


if manual_emotion != "-- None --":

    final_emotion = manual_emotion

elif detected_emotion:

    final_emotion = detected_emotion


# ============================================================
# RECOMMENDATIONS
# ============================================================

if final_emotion:

    accent = MOOD_COLORS.get(
        final_emotion,
        "#6C5CE7"
    )

    # --------------------------------------------------------
    # Dynamic mood styling
    # --------------------------------------------------------

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
            border-radius: 8px;
        }}

        div.stButton > button:hover {{
            background-color: {accent}CC;
            color: white;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Generate query only when emotion changes
    # --------------------------------------------------------

    if (
        st.session_state.current_emotion
        != final_emotion
    ):

        st.session_state.current_emotion = (
            final_emotion
        )

        st.session_state.current_query = (
            get_query_for_emotion(
                final_emotion
            )
        )

    query = st.session_state.current_query

    st.info(
        f"🎯 Current mood: **"
        f"{final_emotion.upper()}**"
    )

    st.caption(
        f"🔎 Searching for: *{query}*"
    )

    # --------------------------------------------------------
    # Music search
    # --------------------------------------------------------

    with st.spinner(
        "🎵 Finding songs for your mood..."
    ):

        songs = get_songs(query)

    st.caption(
        f"🎵 Found {len(songs)} tracks"
    )

    # --------------------------------------------------------
    # Mood history
    # --------------------------------------------------------

    if (
        not st.session_state.history
        or
        st.session_state.history[-1]["emotion"]
        != final_emotion
    ):

        st.session_state.history.append(
            {
                "emotion": final_emotion,
                "songs": songs,
            }
        )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    st.subheader(
        "🎧 Recommended for you"
    )

    if not songs:

        st.warning(
            "No songs found for this mood right now."
        )

    # --------------------------------------------------------
    # Song cards
    # --------------------------------------------------------

    for song in songs:

        song_key = (
            song.get("previewUrl")
            or song.get("title")
        )

        is_open = (
            st.session_state.expanded_song
            == song_key
        )

        with st.expander(
            f"🎵 {song['title']} — "
            f"{song['artist']}",
            expanded=is_open
        ):

            # ----------------------------------------------
            # Explanation
            # ----------------------------------------------

            st.caption(
                f"💡 "
                f"{get_explanation_for_emotion(
                    final_emotion
                )}"
            )

            # ----------------------------------------------
            # Artwork
            # ----------------------------------------------

            if song.get("thumbnail"):

                st.image(
                    song["thumbnail"],
                    width=150
                )

            # ----------------------------------------------
            # Audio preview
            # ----------------------------------------------

            if song.get("previewUrl"):

                st.audio(
                    song["previewUrl"]
                )

                st.caption(
                    "▶️ 30-second preview"
                )

            else:

                st.caption(
                    "No preview available."
                )

            # ----------------------------------------------
            # YouTube
            # ----------------------------------------------

            if song.get("youtubeUrl"):

                st.link_button(
                    "▶️ Watch Full Song on YouTube",
                    song["youtubeUrl"]
                )

            # ----------------------------------------------
            # Bookmark
            # ----------------------------------------------

            already_bookmarked = any(
                b.get("previewUrl")
                == song.get("previewUrl")
                and
                b["title"]
                == song["title"]

                for b in st.session_state.bookmarks
            )

            if already_bookmarked:

                st.success(
                    "❤️ Bookmarked"
                )

            else:

                if st.button(
                    "🤍 Bookmark this song",
                    key=(
                        f"bookmark_"
                        f"{song_key}_"
                        f"{song['title']}"
                    )
                ):

                    st.session_state.bookmarks.append(
                        song
                    )

                    st.session_state.expanded_song = (
                        song_key
                    )

                    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎵 MoodTunes • "
    "Music that understands how you feel."
)
