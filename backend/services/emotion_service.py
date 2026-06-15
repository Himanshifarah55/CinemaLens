from transformers import pipeline

print("Loading emotion model...")

emotion_classifier = pipeline(
    task="text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
    device=-1
)

print("Emotion model loaded.")


def analyze_emotions(text: str) -> dict:

    results = emotion_classifier(text)[0]

    emotions = {}

    for item in results:

        emotions[item["label"]] = round(
            item["score"],
            4
        )

    return emotions