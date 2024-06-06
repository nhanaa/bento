import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "react-query";
import axios from "axios";

interface AuthButtonProps {
  brand: string;
  imgUrl: string;
}

function capitalize(word: string): string {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

export const AuthButton: React.FC<AuthButtonProps> = ({ brand, imgUrl }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const exchangeCodeForToken = async (code: string) => {
    console.log(`Exchanging code for token with code: ${code}`);
    const response = await axios.post(
      `http://127.0.0.1:5000/oauth/${brand}/callback`,
      { code }
    );
    return response.data;
  };

  const mutation = useMutation(exchangeCodeForToken, {
    onSuccess: (data) => {
      console.log(`Token received: ${data.token}`);
      localStorage.setItem("token", data.token);
      navigate("/home");
    },
    onError: (error) => {
      console.error("Error exchanging code for token:", error);
    },
  });

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const code = queryParams.get("code");
    if (code) {
      mutation.mutate(code);
    }
  }, [location.search]);

  const handleAuthClick = () => {
    console.log(`Redirecting to OAuth login for ${brand}`);
    window.location.href = `http://127.0.0.1:5000/oauth/${brand}/login`;
  };

  return (
    <div
      className="flex flex-row items-center text-gray-500 bg-white hover:bg-gray-50 transition-colors font-medium border border-gray-200 rounded-xl shadow px-5 py-3 gap-5 cursor-pointer"
      onClick={handleAuthClick}
    >
      <img className="w-4 h-4" src={imgUrl} />
      Continue with {capitalize(brand)}
    </div>
  );
};
