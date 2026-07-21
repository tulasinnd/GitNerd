import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Learning from "./pages/Learning";

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
    </Routes>
  );
}

export default App;