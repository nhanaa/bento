import { useUser } from "@/contexts/UserContext";
import React from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute: React.FC<{ children: React.ReactElement }> = ({
  children,
}) => {
  const { user } = useUser();

  if (!user) {
    return <Navigate to="/auth" />;
  }

  return children;
};

export default PrivateRoute;
