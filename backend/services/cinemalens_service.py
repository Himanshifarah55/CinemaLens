from backend.services.review_analyzer import analyze_review
from backend.services.emotion_service import analyze_emotions
from backend.services.lime_service import get_lime_explanation


def analyze_complete_review(review: str):

    aspect_results = analyze_review(review)

    emotions = analyze_emotions(review)

    final_aspects = []

    for result in aspect_results:

        aspect_name = result["aspect"]

        explanation = get_lime_explanation(
            review,
            aspect_name
        )

        final_aspects.append(
            {
                **result,
                "explanation": explanation[:5]
            }
        )

    return {
        "aspects": final_aspects,
        "emotions": emotions
    }