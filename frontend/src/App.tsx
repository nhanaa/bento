import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Homepage from "./pages/Homepage";
import FolderView from "./pages/FolderView";
import { Auth } from "./pages/Auth";
import { Landing } from "./pages/Landing";
import PrivateRoute from "./components/PrivateRoute";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route
          path="/home"
          element={
            <PrivateRoute>
              <Homepage />
            </PrivateRoute>
          }
        />
        <Route
          path="/folder/:folderId"
          element={
            <PrivateRoute>
              <FolderView />
            </PrivateRoute>
          }
        />
        <Route path="/auth" element={<Auth />} />
        <Route path="/" element={<Landing />} />
      </Routes>
    </Router>
  );
};

export default App;
