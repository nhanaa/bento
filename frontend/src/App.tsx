import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Homepage from "./pages/Homepage";
import FolderView from "./pages/FolderView";
import { Auth } from "./pages/Auth";
import { Landing } from "./pages/Landing";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/home" element={<Homepage />} />
        <Route path="/folder" element={<FolderView />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/" element={<Landing />} />
      </Routes>
    </Router>
  );
};

export default App;
