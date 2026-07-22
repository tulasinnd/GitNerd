import "../App.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const [githubUrl, setGithubUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [loadingRepository, setLoadingRepository] = useState(false);
  const [loadingLearning, setLoadingLearning] = useState(false);

  const [loadingInterview, setLoadingInterview] = useState(false);

  async function validateRepository() {
    setError("");
    setResult(null);
    setLoadingRepository(true);

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

      if (data.success) {
        setSessionId(data.session_id);
      }
    } catch (err) {
      setResult(null);
      setError("Unable to connect to the backend.");
    } finally {
      setLoadingRepository(false);
    }
  }

  async function learnRepository() {
    setLoadingLearning(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/learning", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
        }),
      });

      const data = await response.json();

    //   if (data.success) {
    //     navigate(`/learning/${sessionId}`);
    //   }
    if (data.success) {
    window.open(`/learning/${sessionId}`, "_blank");
}
    } catch (error) {
      console.error(error);
    }finally {

        setLoadingLearning(false);

    }

  }

  async function interviewRepository() {
    setLoadingInterview(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/interview", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
        }),
      });

      const data = await response.json();

      if (data.success) {
        window.open(`/interview/${sessionId}`, "_blank");
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingInterview(false);
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
          onChange={(e) => {
            setGithubUrl(e.target.value);
            setError("");
            setResult(null);
          }}
        />

        <button
          onClick={validateRepository}
          disabled={loadingRepository}
        >
          {loadingRepository
            ? "Exploring Repository..."
            : "Explore Repository"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {result && !result.success && (
        <p className="error">{result.message}</p>
      )}

      {result && result.success && (
        <div className="repository-summary">
          <h2>Repository Summary</h2>

          <p>{result.repository_summary}</p>

          <div className="repository-actions">
            <button
                onClick={learnRepository}
                disabled={loadingLearning}
            >
                {loadingLearning
                    ? "Preparing Repository..."
                    : "Learn Repository"}
            </button>

              <button
                  onClick={interviewRepository}
                  disabled={loadingInterview}
                >
                  {loadingInterview
                    ? "Preparing Interview..."
                    : "Interview Simulation"}
                </button>
          </div>
        </div>
      )}

      {loadingLearning && (
          <div className="learning-loading">
              <div className="spinner"></div>

              <p>
                  GitNerd is reading and understanding the entire repository.
                  This may take a minute depending on the repository size.
              </p>
          </div>
      )}

      {loadingInterview && (
        <div className="learning-loading">
          <div className="spinner"></div>

          <p>
            GitNerd is preparing your repository interview.
            This may take a moment.
          </p>
        </div>
      )}
    </div>

  );
}

export default Home;