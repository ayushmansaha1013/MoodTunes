AI-powered music recommendations based on your facial emotion.

MoodTunes uses real-time facial emotion detection to understand how you're feeling and instantly recommends music that matches your mood — no manual searching, no playlists to scroll through. Just show your face, and let the AI do the rest.

💡 Inspiration

Music discovery today is either fully manual (you search, you scroll, you pick) or based on listening history, which doesn't capture how you're feeling right now. MoodTunes closes that gap — using computer vision to read your current emotional state and translate it directly into a music recommendation, in seconds.

⚙️ How It Works
Capture — User takes a photo via webcam (or selects a mood manually as a fallback)
Detect — DeepFace analyzes the image and classifies the dominant emotion (happy, sad, angry, fear, surprise, neutral, disgust)
Map — The detected emotion is mapped to a curated music search query (e.g. happy → "upbeat pop hits")
Recommend — ytmusicapi searches YouTube Music and returns matching songs
Play — Songs are embedded directly in the app for instant playback
🛠️ Tech Stack
Layer	Technology
Emotion Detection	OpenCV + DeepFace
Music Search	ytmusicapi (no API key required)
Frontend / UI	Streamlit
Backend	Python
✨ Features
📷 Live webcam emotion detection — real-time facial analysis, no setup required
🎯 Manual mood override — a dropdown fallback if face detection struggles with lighting/angle, ensuring the demo never breaks
🎧 Embedded music playback — songs play directly inside the app, no tab-switching
📜 Session mood history — tracks every mood detected during your session
❤️ Bookmarking — save songs you like for quick access later in the session
🆓 Zero paid APIs — no YouTube Data API key, no quotas, no billing setup
