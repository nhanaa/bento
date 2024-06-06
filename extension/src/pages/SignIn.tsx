import React from "react";
import logo from "../../public/icon.svg";
import { AuthButton } from "@/components/signin/AuthButton";
import { Link } from "react-router-dom";

function SignIn() {
  return (
    <div className="w-full bg-customWhite flex-col items-center justify-center py-8 px-6 space-y-5">
      <div className="w-full flex items-center justify-center">
        <img src={logo} alt="logo" height="44px" width="40px" />
      </div>
      <h1 className="w-full font-bold text-center text-gray-800">Sign In</h1>
      <div className="space-y-2">
        <AuthButton
          brand="Google"
          imgUrl="https://cdn.iconscout.com/icon/free/png-256/free-google-1772223-1507807.png"
        />
        <AuthButton
          brand="GitHub"
          imgUrl="https://cdn-icons-png.flaticon.com/512/25/25231.png"
        />
      </div>
      <p className="w-full text-center">
        Don't have an account?{" "}
        <Link to="/dashboard" className="hover:underline">
          Sign up
        </Link>
      </p>
    </div>
  );
}

export default SignIn;
