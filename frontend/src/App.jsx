import { useState } from "react";

// Where your FastAPI server is running (from Phase 5)
const API_URL = "http://127.0.0.1:8000/ask";

// The exact scheme_id values used in your data (from schemes_raw.py)
const SCHEMES = [
  { id: "", label: "All schemes (no filter)" },
  { id: "csss", label: "CSSS" },
  { id: "aicte_pragati", label: "AICTE Pragati" },
  { id: "aicte_saksham", label: "AICTE Saksham" },
  { id: "mcm", label: "Merit-cum-Means (MCM)" },
  { id: "post_matric_sc", label: "Post-Matric (SC)" },
  { id: "post_matric_st", label: "Post-Matric (ST)" },
  { id: "post_matric_obc", label: "Post-Matric (OBC)" },
  { id: "post_matric_minority", label: "Post-Matric (Minority)" },
];

function App() {
  const [question, setQuestion] = useState("");
  const [selectedScheme, setSelectedScheme] = useState("");  // "" means no filter
  const [result, setResult] = useState(null);   // will hold {answer, sources, confident}
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;   // don't send empty questions

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: question,
          // "" (no filter selected) becomes null; otherwise send the chosen scheme_id
          scheme_id: selectedScheme === "" ? null : selectedScheme,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      // This runs if the server can't be reached at all (e.g. not running, CORS issue)
      setResult({
        answer: "Could not reach the server. Is app.py running?",
        sources: [],
        confident: false,
      });
    }

    setLoading(false);
  }

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Government Scheme Assistant</h2>

      <select
        value={selectedScheme}
        onChange={(e) => setSelectedScheme(e.target.value)}
        style={{ width: "100%", padding: "8px", fontSize: "14px", marginBottom: "10px" }}
      >
        {SCHEMES.map((scheme) => (
          <option key={scheme.id} value={scheme.id}>
            {scheme.label}
          </option>
        ))}
      </select>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about CSSS, Pragati, Saksham, MCM, or Post-Matric schemes..."
        rows={3}
        style={{ width: "100%", padding: "10px", fontSize: "16px" }}
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        style={{ marginTop: "10px", padding: "10px 20px", fontSize: "16px" }}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {/* Only show a result box once we actually have a result */}
      {result && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            borderRadius: "8px",
            backgroundColor: result.confident ? "#eaffea" : "#fff3e0",
            border: result.confident ? "1px solid #4caf50" : "1px solid #ff9800",
          }}
        >
          <p style={{ margin: 0 }}>{result.answer}</p>

          {!result.confident && (
            <p style={{ fontSize: "13px", color: "#e65100", marginTop: "10px" }}>
              ⚠ Low confidence answer
            </p>
          )}

          {result.sources.length > 0 && (
            <p style={{ fontSize: "13px", color: "#555", marginTop: "10px" }}>
              Sources: {result.sources.join(", ")}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;