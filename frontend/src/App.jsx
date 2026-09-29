import { useEffect, useState } from "react";

// A component is a function that returns what should appear on screen.
// useState gives it memory: when a state value changes, React redraws.
export default function App() {
  const [topics, setTopics] = useState([]);
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [question, setQuestion] = useState(null);
  const [picked, setPicked] = useState(null); // index of the option the user clicked
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // useEffect with [] runs once, when the page first loads.
  useEffect(() => {
    fetch("/api/topics")
      .then((res) => res.json())
      .then((list) => {
        setTopics(list);
        setTopic(list[0]);
      })
      .catch(() => setError("Could not reach the backend. Is it running?"));
  }, []);

  async function getQuestion() {
    setLoading(true);
    setError("");
    setPicked(null);
    try {
      const res = await fetch("/api/questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, difficulty }),
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
      setQuestion(await res.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>QuizMe</h1>
      <p>Test yourself on system design concepts.</p>

      <div className="controls">
        <select value={topic} onChange={(e) => setTopic(e.target.value)}>
          {topics.map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        <button onClick={getQuestion} disabled={loading || !topic}>
          {loading ? "Thinking..." : "New question"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {question && (
        <section className="card">
          <h2>{question.question}</h2>
          <ol className="options">
            {question.options.map((option, i) => {
              // After the user picks, colour the right answer green and a wrong pick red.
              let className = "";
              if (picked !== null && i === question.correct_index) className = "correct";
              else if (i === picked) className = "wrong";
              return (
                <li key={i}>
                  <button
                    className={className}
                    onClick={() => setPicked(i)}
                    disabled={picked !== null}
                  >
                    {option}
                  </button>
                </li>
              );
            })}
          </ol>
          {picked !== null && (
            <p className="explanation">
              <strong>{picked === question.correct_index ? "Correct! " : "Not quite. "}</strong>
              {question.explanation}
            </p>
          )}
        </section>
      )}
    </main>
  );
}
