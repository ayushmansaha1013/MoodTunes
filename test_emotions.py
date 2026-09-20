from deepface import DeepFace

result = DeepFace.analyze(img_path=r"C:\Users\indra\Downloads\MoodTunes\test.jpg", actions=['emotion'], enforce_detection=False)
print(result)