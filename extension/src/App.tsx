import React from 'react';
import { RouterProvider, createHashRouter } from 'react-router-dom';
import SignIn from './pages/SignIn';
import Dashboard from './pages/Dashboard';

const router = createHashRouter([
  {
    path: "/",
    element: <SignIn />,
  },
  {
    path: "/dashboard",
    element: <Dashboard />
  }
])
function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
