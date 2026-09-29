"""Data shapes shared by the API and the AI code.

Pydantic models describe what a piece of JSON looks like. FastAPI uses them to
check incoming requests and to document the API at /docs automatically.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Difficulty = Literal["easy", "medium", "hard"]


class QuestionRequest(BaseModel):
    """What the frontend sends when it wants a new question."""

    topic: str = Field(min_length=2, max_length=100)
    difficulty: Difficulty = "medium"


class Question(BaseModel):
    """One multiple-choice question, with its answer and an explanation."""

    # extra="forbid" means "no fields other than these", which the Claude API
    # needs so it can force its reply to match this exact shape.
    model_config = ConfigDict(extra="forbid")

    question: str
    options: list[str]
    correct_index: int
    explanation: str
