"""Tests run with:  pytest

TestClient lets us call the API like a browser would, without starting a server.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_topics_are_listed():
    response = client.get("/api/topics")
    assert "Caching" in response.json()


def test_question_without_api_key_returns_sample(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    response = client.post("/api/questions", json={"topic": "Load balancing"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["options"]) == 4
    assert 0 <= body["correct_index"] < 4


def test_bad_difficulty_is_rejected():
    response = client.post("/api/questions", json={"topic": "Caching", "difficulty": "impossible"})
    assert response.status_code == 422
