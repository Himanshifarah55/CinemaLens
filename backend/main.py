from backend.api.schemas import ReviewRequest
from backend.services.cinemalens_service import analyze_complete_review
from fastapi import FastAPI

app = FastAPI(
    title="CinemaLens API",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "CinemaLens API Running"
    }

@app.post("/analyze")
def analyze_review(request: ReviewRequest):

    result = analyze_complete_review(
        request.review
    )

    return result