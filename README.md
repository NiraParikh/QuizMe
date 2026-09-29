# QuizMe

Quiz yourself on system design concepts. Claude writes each question, the
answer, and an explanation.

- `backend/` is Python with [FastAPI](https://fastapi.tiangolo.com/).
- `frontend/` is [React](https://react.dev/) built with [Vite](https://vite.dev/).

## Run it locally

You need Python 3.10+ and Node 20+. Use two terminals.

**Terminal 1: backend**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # optional, see below
fastapi dev app/main.py
```

The API runs at http://localhost:8000. Open http://localhost:8000/docs to try it.

Without `ANTHROPIC_API_KEY` the backend returns one built-in sample question,
so you can explore the app for free. Set the key to get real AI questions.
Never commit your key.

**Terminal 2: frontend**

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## Tests

```bash
cd backend && pytest
```

## How the pieces fit

1. The React page (`frontend/src/App.jsx`) calls `POST /api/questions` with a topic.
2. FastAPI (`backend/app/main.py`) receives it and calls `generate_question`.
3. `backend/app/ai.py` asks Claude for a question in a fixed JSON shape
   (`backend/app/models.py`) and sends it back to the page.
