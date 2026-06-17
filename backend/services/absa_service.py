from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch

MODEL_NAME = "yangheng/deberta-v3-base-absa-v1.1"

print("Loading ABSA model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)

print("ABSA model loaded.")


def classify_aspect(
    review: str,
    aspect: str
) -> dict:

    inputs = tokenizer(
        aspect,
        review,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(
        outputs.logits,
        dim=-1
    )[0]

    predicted_idx = torch.argmax(
        probs
    ).item()

    sentiment = model.config.id2label[
        predicted_idx
    ]

    confidence = float(
        probs[predicted_idx]
    )

    return {
        "aspect": aspect,
        "sentiment": sentiment.lower(),
        "confidence": round(confidence, 4)
    }