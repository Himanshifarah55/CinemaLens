from backend.api.schemas import ReviewRequest
from backend.services.cinemalens_service import analyze_complete_review
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CinemaLens API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "CinemaLens API Running"
    }

@app.post("/analyze")
def analyze_review_endpoint(
    request: ReviewRequest
):

    result = analyze_complete_review(
        request.review
    )

    return result