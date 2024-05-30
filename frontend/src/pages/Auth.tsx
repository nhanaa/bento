import React, { useState } from "react";
import logo from "/icon.svg";
import { AuthButtons } from "@/components/auth/AuthButtons";

export const Auth: React.FC = () => {
  const [pageView, setPageView] = useState("signup"); 

  const togglePageView = () => {
    setPageView((prevView) => (prevView === "signup" ? "login" : "signup"));
  };

  return (
    <div className="h-screen w-screen p-10 flex flex-col items-center justify-center gap-5">
      <img src={logo} width={100} alt="icon" />
      <h1 className="font-bold">
        {pageView === "signup" ? "Sign up" : "Log in"}
      </h1>
      <p className="font-medium text-gray-500">To continue using Bento</p>
      <AuthButtons />
      {pageView === "signup" ? (
        <p className="font-medium text-gray-500">
          Have an account?{" "}
          <span
            className="text-customViolet-500 hover:underline cursor-pointer"
            onClick={togglePageView}
          >
            Log in
          </span>
        </p>
      ) : (
        <p className="font-medium text-gray-500">
          Don't have an account?{" "}
          <span
            className="text-customViolet-500 hover:underline cursor-pointer"
            onClick={togglePageView}
          >
            Sign up
          </span>
        </p>
      )}
    </div>
  );
};
