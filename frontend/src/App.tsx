import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Homepage from "./pages/Homepage";
import FolderView from "./pages/FolderView";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/folder" element={<FolderView />} />
      </Routes>
    </Router>
  );
};

export default App;
