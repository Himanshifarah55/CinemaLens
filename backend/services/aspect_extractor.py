import spacy

nlp = spacy.load("en_core_web_sm")

MOVIE_ASPECTS = {
    "acting",
    "performance",
    "plot",
    "story",
    "music",
    "soundtrack",
    "direction",
    "director",
    "screenplay",
    "dialogue",
    "character",
    "cinematography",
    "visual",
    "effects",
    "ending",
    "pacing",
    "scene"
}


def extract_aspects(text: str) -> list[str]:
    doc = nlp(text.lower())

    found = set()

    for token in doc:
        if token.pos_ not in {
            "NOUN",
            "PROPN"
        }:
            continue
        lemma = token.lemma_

        if lemma in MOVIE_ASPECTS:
            found.add(lemma)

    if found:
        return list(found)

    return ["overall"]