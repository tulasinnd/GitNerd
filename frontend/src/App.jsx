import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Learning from "./pages/Learning";
import Interview from "./pages/Interview";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<Home />}
      />

      <Route
        path="/learning/:sessionId"
        element={<Learning />}
      />

      <Route
        path="/interview/:sessionId"
        element={<Interview />}
      />
    </Routes>
  );
}

export default App;