"""Asks Claude to write a quiz question.

If no ANTHROPIC_API_KEY is set, we return a built-in sample question instead,
so you can run and play with the app without a key (and without cost).
"""

import json
import os

import anthropic

from .models import Difficulty, Question

MODEL = "claude-opus-5-5"

SAMPLE_QUESTION = Question(
    question="What is the main job of a load balancer?",
    options=[
        "Store user sessions permanently",
        "Spread incoming requests across several servers",
        "Encrypt data in the database",
        "Compile code before deployment",
    ],
    correct_index=1,
    explanation=(
        "A load balancer sits in front of a group of servers and sends each "
        "request to one of them, so no single server gets overwhelmed and the "
        "system keeps working if one server fails."
    ),
)

PROMPT = """You are a friendly system design tutor writing quiz questions.

Write ONE multiple-choice question about this system design topic: {topic}
Difficulty: {difficulty}

Rules:
- Exactly 4 options, only one of them correct.
- correct_index is the 0-based position of the correct option.
- The explanation says why the right answer is right and why the most
  tempting wrong answer is wrong, in 2 to 4 plain sentences.
"""


def generate_question(topic: str, difficulty: Difficulty) -> Question:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return SAMPLE_QUESTION

    # The client reads ANTHROPIC_API_KEY from the environment by itself.
    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[
            {"role": "user", "content": PROMPT.format(topic=topic, difficulty=difficulty)}
        ],
        # Force the reply to be JSON shaped exactly like our Question model.
        output_config={
            "effort": "low",
            "format": {"type": "json_schema", "schema": Question.model_json_schema()},
        },
        # If this model declines a request, let the API retry on another model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )

    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined to write a question on that topic.")

    text = next(block.text for block in response.content if block.type == "text")
    question = Question.model_validate(json.loads(text))

    # Double-check the answer really points at one of the options.
    if len(question.options) != 4 or not 0 <= question.correct_index < 4:
        raise RuntimeError("Claude returned a malformed question; please try again.")
    return question
