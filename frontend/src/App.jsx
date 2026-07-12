import './App.css'
import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  async function getBackendData() {
    try {
      const response = await fetch("http://127.0.0.1:8000/");
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError("Failed to connect to backend.");
    }
  }

  useEffect(() => {
    getBackendData();
  }, []);

  return (
    <div>
      <h1>GitNerd</h1>

      {error && <p>{error}</p>}

      {data && (
        <>
          <p>App: {data.app}</p>
          <p>Status: {data.status}</p>
        </>
      )}
    </div>
  );
}

export default App;