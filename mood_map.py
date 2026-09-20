import random

EMOTION_EXPLANATIONS = {
    'happy':    "An upbeat track to match your positive energy.",
    'sad':      "A gentle, emotional song to sit with how you're feeling.",
    'angry':    "A high-intensity track to channel that energy.",
    'fear':     "A calming, soothing pick to help you relax.",
    'surprise': "A high-energy track to match your excitement.",
    'neutral':  "A relaxed, easy-listening pick for your mood.",
    'disgust':  "A calming track to help reset your mood.",
}

EMOTION_TO_QUERY = {
    'happy':    ["upbeat pop", "happy hits", "feel good playlist", "cheerful acoustic"],
    'sad':      ["melancholy acoustic", "sad indie ballads", "somber piano", "emotional songs"],
    'angry':    ["high energy rock", "heavy metal workout", "intense phonk", "hard rock"],
    'fear':     ["calming ambient", "soothing relaxing music", "peaceful piano", "stress relief music"],
    'surprise': ["exciting EDM", "energetic dance pop", "hype music", "upbeat synthwave"],
    'neutral':  ["chill lo-fi beats", "relaxing jazz hop", "easy listening", "background acoustic"],
    'disgust':  ["deep reset ambient", "clean focus music", "calm instrumental", "meditation soundscapes"],
}


def get_explanation_for_emotion(emotion: str) -> str:
    return EMOTION_EXPLANATIONS.get(emotion, "A track picked to match your mood.")

def get_query_for_emotion(emotion: str) -> str:
    """Returns a random search query matching the given emotion."""
    options = EMOTION_TO_QUERY.get(emotion, ["popular music"])
    return random.choice(options)


# Quick test when run directly
if __name__ == "__main__":
    test_emotions = ['happy', 'sad', 'angry', 'neutral', 'fear', 'surprise', 'disgust']
    for emo in test_emotions:
        print(f"{emo} -> {get_query_for_emotion(emo)}")