from lime.lime_text import LimeTextExplainer
import torch
import numpy as np
from backend.services.absa_service import tokenizer, model


class_names = [
    model.config.id2label[i].lower()
    for i in range(
        len(model.config.id2label)
    )
]

explainer = LimeTextExplainer(
    class_names=class_names
)

def get_lime_explanation(
    review: str,
    aspect: str
):

    def predict_proba(texts):

        inputs = tokenizer(
            [aspect] * len(texts),
            texts,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.softmax(
            outputs.logits,
            dim=-1
        )

        return probs.numpy()

    prediction = predict_proba(
        [review]
    )

    predicted_class = prediction[
        0
    ].argmax()

    explanation = explainer.explain_instance(
        review,
        predict_proba,
        labels=[predicted_class],
        num_features=10,
        num_samples=200
    )

    explanation_list = []

    for word, weight in explanation.as_list(
        label=predicted_class
    ):

        if len(word) <= 2:
            continue

        if word.lower() in {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "to",
            "of",
            "in",
            "on",
            "at",
            "for",
            "with"
        }:
            continue

        explanation_list.append(
            {
                "word": str(word),
                "weight": round(
                    float(weight),
                    4
                )
            }
        )

    return explanation_list