import streamlit as st
import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)
from backend.services.cinemalens_service import (
    analyze_complete_review
)

st.set_page_config(
    page_title="CinemaLens",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CinemaLens")
st.write("Explainable Aspect-Based Sentiment Analysis")

review = st.text_area(
    "Enter a movie review",
    height=200,
    placeholder="The acting was phenomenal but the plot was boring and the music was forgettable..."
)

if st.button("Analyze Review"):

    if not review.strip():

        st.warning("Please enter a review.")

    else:

        with st.spinner("Analyzing review..."):

            result = analyze_complete_review(
                review
            )

        st.subheader("Aspect Analysis")

        for aspect in result["aspects"]:

            st.write(
                f"🎬 Aspect: {aspect['aspect'].title()}"
            )

            sentiment = aspect["sentiment"]
            if sentiment == "positive":
                st.success(f"🟢 {sentiment.title()}")

            elif sentiment == "negative":
                st.error(f"🔴 {sentiment.title()}")

            else:
                st.info(f"⚪ {sentiment.title()}")

            st.write(
                f"Confidence: {aspect['confidence'] * 100:.2f}%"
            )
            st.write("### Why did the AI think this?")

            for explanation in aspect["explanation"]:
                word = explanation["word"]
                weight = explanation["weight"]

                if len(word) <= 2:
                    continue

                if word.lower() in {
                    "the",
                    "a",
                    "an",
                    "and",
                    "but",
                    "was",
                    "were",
                    "is",
                    "are"
                }:
                    continue

                

                if weight > 0:

                    st.success(
                        f"{word} (+{weight:.4f})"
                    )

                else:

                    st.error(
                        f"{word} ({weight:.4f})"
                    )

            st.divider()
        
        emotions = result["emotions"]

        top_emotion = max(
            emotions,
            key=emotions.get
        )

        top_score = emotions[top_emotion]

        st.info(
            f"🎭 Dominant Emotion: {top_emotion.title()} ({top_score * 100:.2f}%)"
        )

        st.subheader("Emotion Analysis")

        emotions = result["emotions"]

        sorted_emotions = sorted(
            emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for emotion, score in sorted_emotions:

            st.write(
                f"**{emotion.title()}** ({score * 100:.2f}%)"
            )

            st.progress(float(score))