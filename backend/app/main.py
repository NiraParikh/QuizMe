"""The web server. Run it with:  fastapi dev app/main.py

Each function below decorated with @app.get or @app.post becomes a URL the
frontend can call. Open http://localhost:8000/docs to try them in the browser.
"""

from fastapi import FastAPI, HTTPException

from .ai import generate_question
from .models import Question, QuestionRequest

app = FastAPI(title="QuizMe API")

TOPICS = [
    "Load balancing",
    "Caching",
    "Database sharding",
    "Replication",
    "CAP theorem",
    "Message queues",
    "Rate limiting",
    "Consistent hashing",
    "CDNs",
    "Microservices vs monoliths",
]


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/topics")
def list_topics() -> list[str]:
    return TOPICS


@app.post("/api/questions")
def create_question(request: QuestionRequest) -> Question:
    try:
        return generate_question(request.topic, request.difficulty)
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error))
