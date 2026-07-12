import './App.css'
import { useEffect, useState } from "react";

function App() {
  const [githubUrl, setGithubUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function validateRepository() {
    try {
      const response = await fetch("http://127.0.0.1:8000/repository", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          github_url: githubUrl,
        }),
      });

      const data = await response.json();

      setResult(data);
      setError("");
    } catch (err) {
      setResult(null);
      setError("Failed to connect to backend.");
    }
  }
return (
  <div className="app">
    <h1>GitNerd</h1>
    <p className="subtitle">
      AI-powered repository learning and interview platform.
    </p>

    <div className="repository-input">
      <input
        type="text"
        placeholder="https://github.com/owner/repository"
        value={githubUrl}
        onChange={(e) => setGithubUrl(e.target.value)}
      />

      <button onClick={validateRepository}>
        Validate Repository
      </button>
    </div>

    {error && <p className="error">{error}</p>}

    {result && (
      <p className={result.valid ? "success" : "error"}>
        {result.message}
      </p>
    )}
  </div>
);


}

export default App;