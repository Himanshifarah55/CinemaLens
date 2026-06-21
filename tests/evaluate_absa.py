import sys
from pathlib import Path
import time
import xml.etree.ElementTree as ET

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from backend.services.absa_service import (
    classify_aspect
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


DATASET_PATH = "datasets/Restaurants_Train_v2.xml"

print("Loading dataset...")

tree = ET.parse(DATASET_PATH)
root = tree.getroot()

y_true = []
y_pred = []

start_time = time.time()

print("Starting evaluation...\n")

for sentence in root.findall("sentence"):

    text_element = sentence.find("text")

    if text_element is None:
        continue

    review = text_element.text

    aspect_terms = sentence.find("aspectTerms")

    if aspect_terms is None:
        continue

    for aspect_term in aspect_terms:

        true_sentiment = aspect_term.attrib.get(
            "polarity"
        )

        if true_sentiment == "conflict":
            continue

        aspect = aspect_term.attrib.get(
            "term"
        )

        try:

            prediction = classify_aspect(
                review,
                aspect
            )

            predicted_sentiment = prediction[
                "sentiment"
            ]

            y_true.append(
                true_sentiment
            )

            y_pred.append(
                predicted_sentiment
            )

        except Exception as e:

            print(
                f"Error on aspect '{aspect}': {e}"
            )

            continue

end_time = time.time()

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision, recall, f1, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted"
    )
)

print("\n" + "=" * 50)
print("SEMEVAL 2014 ABSA EVALUATION")
print("=" * 50)

print(
    f"\nTotal Evaluated Samples: {len(y_true)}"
)

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)

print(
    f"Execution Time: {end_time - start_time:.2f} seconds"
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_true,
        y_pred
    )
)

# -------------------------
# Confusion Matrix
# -------------------------

labels = [
    "negative",
    "neutral",
    "positive"
]

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=labels
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot()

plt.title(
    "CinemaLens - SemEval 2014 ABSA"
)

plt.savefig(
    "tests/confusion_matrix.png",
    bbox_inches="tight"
)

print(
    "\nConfusion matrix saved to:"
)

print(
    "tests/confusion_matrix.png"
)

plt.show()