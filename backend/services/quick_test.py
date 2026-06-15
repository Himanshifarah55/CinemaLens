from cinemalens_service import analyze_complete_review

review = (
    "The acting was phenomenal "
    "but the plot was boring "
    "and the music was forgettable."
)

result = analyze_complete_review(review)

print(result)