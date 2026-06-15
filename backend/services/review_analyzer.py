from backend.services.aspect_extractor import extract_aspects
from backend.services.absa_service import classify_aspect


def analyze_review(review: str):

    aspects = extract_aspects(review)

    results = []

    for aspect in aspects:

        sentiment_result = classify_aspect(
            review,
            aspect
        )

        results.append(
            sentiment_result
        )

    return results