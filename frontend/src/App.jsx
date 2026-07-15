import "./App.css";
import { useState } from "react";

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
      setError("Unable to connect to the backend.");
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
          Explore Repository
        </button>
      </div>

      {/* Network Error */}
      {error && <p className="error">{error}</p>}

      {/* Backend Error */}
      {result && !result.success && (
        <p className="error">{result.message}</p>
      )}

      {/* Repository Structure */}
      {result && result.success && (
  <div >

    <h2>Repository Analysis</h2>

    <p>
      Files:
      {" "}
      {result.repository_analysis.repository_structure.files.length}
    </p>

    <p>
      Directories:
      {" "}
      {result.repository_analysis.repository_structure.directories.length}
    </p>

    <p>
      Important Files:
      {" "}
      {Object.keys(result.repository_analysis.important_files).join(", ")}
    </p>

  </div>
)}
    </div>
  );
}

export default App;