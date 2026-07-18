// import "./App.css";
// import { useState } from "react";

// function App() {
//   const [githubUrl, setGithubUrl] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState("");

//   async function validateRepository() {
//     try {
//       const response = await fetch("http://127.0.0.1:8000/repository", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           github_url: githubUrl,
//         }),
//       });

//       const data = await response.json();

//       setResult(data);
//       setError("");
//     } catch (err) {
//       setResult(null);
//       setError("Unable to connect to the backend.");
//     }
//   }

//   return (
//     <div className="app">
//       <h1>GitNerd</h1>

//       <p className="subtitle">
//         AI-powered repository learning and interview platform.
//       </p>

//       <div className="repository-input">
//         <input
//           type="text"
//           placeholder="https://github.com/owner/repository"
//           value={githubUrl}
//           onChange={(e) => setGithubUrl(e.target.value)}
//         />

//         <button onClick={validateRepository}>
//           Explore Repository
//         </button>
//       </div>

//       {/* Network Error */}
//       {error && <p className="error">{error}</p>}

//       {/* Backend Error */}
//       {result && !result.success && (
//         <p className="error">{result.message}</p>
//       )}

//       {result && result.success && (
//   <div className="repository-summary">
//     <h2>Repository Summary</h2>

//     <p>{result.repository_summary}</p>
//   </div>
// )}
//     </div>
//   );
// }

// export default App;

import "./App.css";
import { useState } from "react";

function App() {
  const [githubUrl, setGithubUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState("");

  const [showLearning, setShowLearning] = useState(false);
  const [learningResult, setLearningResult] = useState(null);

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

    // Store the learning response
    setLearningResult(data);

    // Show the learning section
    setShowLearning(true);

    // Smoothly scroll to it
    setTimeout(() => {
      document
        .getElementById("learning-section")
        ?.scrollIntoView({ behavior: "smooth" });
    }, 100);

  } catch (error) {
    console.error(error);
  }
}
  async function interviewRepository() {
    console.log("Interview Simulation");
    console.log("Session ID:", sessionId);

    // Next milestone:
    // Call POST /interview with the session_id
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
      {showLearning && (
      <div id="learning-section" className="learning-section">
        <div className="learning-header">
          <h1>📘 Repository Learning</h1>

          <p>
            Welcome to your AI-powered learning workspace.
            Ask questions, explore the repository, understand the
            architecture, and learn every part of the project.
          </p>
        </div>

        <div className="learning-content">
          {learningResult && (
            <pre>{JSON.stringify(learningResult, null, 2)}</pre>
          )}
        </div>
      </div>
    )}
    </div>
  );
}

export default App;