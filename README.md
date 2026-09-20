# 🎵 MoodTunes

> **Music that understands how you feel.**

MoodTunes is an AI-powered music recommendation app that detects a user's facial emotion and recommends songs that match their current mood.

Built during a **24-hour hackathon**, MoodTunes combines computer vision, emotion recognition, music discovery, and an interactive Streamlit interface into one simple experience.

## 🚀 Live Demo

**Try MoodTunes:**
Link of Project : https://moodtunes-3erurnuzkdtduxugxw7zam.streamlit.app/

---

## ✨ What It Does

MoodTunes follows a simple pipeline:

```text
📷 Capture Face
      ↓
🧠 DeepFace Emotion Detection
      ↓
😊 Detect Current Emotion
      ↓
🎯 Map Emotion → Music Query
      ↓
🎵 Search Music
      ↓
🎧 Personalized Recommendations
      ↓
▶️ Preview / Full Song on YouTube
```

Instead of asking:

> "What do you want to listen to?"

MoodTunes asks:

> **"How are you feeling right now?"**

---

## 🧠 Features

### 📷 AI Facial Emotion Detection

Capture your face using your webcam and let DeepFace analyze your facial expression.

Supported emotions:

* 😊 Happy
* 😢 Sad
* 😡 Angry
* 😨 Fear
* 😮 Surprise
* 😐 Neutral
* 🤢 Disgust

### 🎯 Multi-Capture Emotion Smoothing

Mood detection can be noisy from a single image.

MoodTunes allows up to **3 captures** and averages the emotion scores to produce a more stable result.

### 🎵 Mood-Based Music Recommendations

Detected emotions are mapped to music search queries.

For example:

```text
Happy → upbeat pop / feel-good music

Sad → emotional / acoustic music

Angry → high-energy rock / intense music

Fear → calming / relaxing music

Surprise → energetic / EDM

Neutral → chill / lo-fi
```

### 🎧 In-App Music Preview

Users can listen to available **30-second previews directly inside the Streamlit app**.

### ▶️ Full Song Discovery

Each recommendation includes a button to find and open the full song on YouTube.

### ❤️ Bookmark Songs

Users can bookmark songs they like during their session.

### 📜 Mood History

MoodTunes keeps track of detected moods during the current session and visualizes the mood trend.

### ⚡ Cached Music Search

Music searches are cached using Streamlit's caching mechanism to reduce unnecessary API requests and make the application more responsive.

---

## 🛠️ Tech Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| 🐍 Python             | Core application logic     |
| 🧠 DeepFace           | Facial emotion recognition |
| 👁️ OpenCV            | Image processing           |
| 🎨 Streamlit          | Web interface              |
| 🎵 Deezer API         | Music search & previews    |
| ▶️ YouTube            | Full-song discovery        |
| 🖼️ Pillow            | Image processing           |
| 🔢 NumPy              | Numerical operations       |
| 🤖 TensorFlow / Keras | DeepFace backend           |

---

## 📂 Project Structure

```text
MoodTunes/
│
├── app.py
│   └── Main Streamlit application
│
├── music.py
│   └── Music search and recommendation retrieval
│
├── mood_map.py
│   └── Emotion → music query mapping
│
├── requirements.txt
│   └── Python dependencies
│
├── packages.txt
│   └── System dependencies for Streamlit deployment
│
└── README.md
    └── Project documentation
```

---

## ⚙️ How It Works

### 1. Capture

The user captures an image using their webcam.

### 2. Emotion Detection

DeepFace analyzes the image and returns emotion confidence scores.

Example:

```text
Happy     72%
Neutral   14%
Surprise   8%
Sad        4%
Angry      2%
```

MoodTunes selects the emotion with the highest average score.

### 3. Mood Mapping

The detected emotion is converted into a music search query.

```python
happy → "upbeat pop"
sad → "melancholy acoustic"
angry → "high energy rock"
```

### 4. Music Discovery

MoodTunes searches for relevant tracks and retrieves:

* Song title
* Artist
* Album artwork
* Audio preview
* Full-song discovery link

### 5. Recommendation

The results are displayed as interactive recommendation cards.

---

## 💻 Run Locally

### Clone the repository

```bash
git clone https://github.com/ayushmansaha1013/MoodTunes.git
cd MoodTunes
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run MoodTunes

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🌐 Deployment

MoodTunes can be deployed using **Streamlit Community Cloud**.

The application uses publicly accessible APIs and does not require a paid music API key for its core music discovery functionality.

---

## 🔐 Privacy

MoodTunes processes the captured image for emotion detection during the application session.

The project is designed as a hackathon prototype and does not require users to create an account.

---

## 🎯 Why MoodTunes?

Traditional music recommendation systems often depend on:

* Listening history
* Explicit ratings
* Search history
* User-selected genres

MoodTunes explores a different interaction:

> **Use the user's current emotional expression as an input for music discovery.**

This makes the recommendation experience more spontaneous and interactive.

---

## 🚀 Future Improvements

Possible future versions could include:

* 🎧 Spotify integration
* 📺 Direct YouTube playlist generation
* 🗣️ Voice-based mood detection
* 🎶 Personalized playlists instead of individual tracks
* 🧠 More sophisticated emotion-to-music mapping
* 📊 Long-term mood analytics
* 📱 Mobile-friendly interface
* 🔊 Context-aware recommendations based on time, activity, and mood
* 👥 Multi-person emotion detection

---

## 🏆 Hackathon Project

**MoodTunes** was developed as a rapid AI-powered prototype during a **24-hour hackathon**.

The project demonstrates how computer vision and generative/personalization concepts can be combined with a simple user interface to create an interactive music experience.

---

## 👨‍💻 Author

**Ayushman Saha**

Engineering Student | AI/ML & Data Science

GitHub:
https://github.com/ayushmansaha1013

---

## ⭐ If You Like MoodTunes

Give the repository a ⭐ and try the live demo!

**Mood detected. Music selected. Vibe started. 🎵**
