import "./App.css";
import { useState } from "react";

function App() {
  const [githubUrl, setGithubUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState("");

  const [showLearning, setShowLearning] = useState(false);
  const [learningQuestion, setLearningQuestion] = useState("");
  const [learningMessages, setLearningMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! 👋 I've finished studying your repository. Ask me anything about the repository architecture, source code, execution flow, technologies, or implementation details. What would you like to explore first?",
    },
  ]);

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

      if (data.success) {
        setSessionId(data.session_id);
      }
    } catch (err) {
      setResult(null);
      setError("Unable to connect to the backend.");
    }
  }

  async function learnRepository() {
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

      if (data.success) {
        setShowLearning(true);

        setTimeout(() => {
          document
            .getElementById("learning-section")
            ?.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function sendLearningQuestion() {
    if (learningQuestion.trim() === "") return;

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/learning/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            question: learningQuestion,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        setLearningMessages((previousMessages) => [
          ...previousMessages,
          {
            role: "user",
            content: learningQuestion,
          },
          {
            role: "assistant",
            content: data.answer,
          },
        ]);

        setLearningQuestion("");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function interviewRepository() {
    console.log("Interview Simulation");
    console.log("Session ID:", sessionId);
  }

  return (
    <div className="app">
      <h1>GitNerd</h1>

      <p className="subtitle">
        AI-powered repository learning and interview platform.
      </p>

      {/* Repository Input */}

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

      {/* Repository Summary */}

      {result && result.success && (
        <div className="repository-summary">

          <h2>Repository Summary</h2>

          <p>{result.repository_summary}</p>

          <div className="repository-actions">

            <button onClick={learnRepository}>
              Learn Repository
            </button>

            <button onClick={interviewRepository}>
              Interview Simulation
            </button>

          </div>

        </div>
      )}

      {/* Repository Learning */}

      {showLearning && (
        <div
          id="learning-section"
          className="learning-section"
        >

          <div className="learning-header">
            <h2>📘 Repository Learning</h2>
          </div>

          <div className="chat-window">

            {learningMessages.map((message, index) => (

              <div
                key={index}
                className={
                  message.role === "assistant"
                    ? "assistant-message"
                    : "user-message"
                }
              >

                <div className="message-title">
                  {message.role === "assistant"
                    ? "🤖 GitNerd"
                    : "🙂 You"}
                </div>

                <div className="message-body">
                  <p>{message.content}</p>
                </div>

              </div>

            ))}

          </div>

          <div className="chat-input">

            <input
              type="text"
              placeholder="Ask anything about this repository..."
              value={learningQuestion}
              onChange={(e) =>
                setLearningQuestion(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendLearningQuestion();
                }
              }}
            />

            <button onClick={sendLearningQuestion}>
              Send
            </button>

          </div>

        </div>
      )}
    </div>
  );
}

export default App;