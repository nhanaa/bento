import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "react-query";
import axios from "axios";

const useAuth = (brand: string) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const exchangeCodeForToken = async (code: string) => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Exchanging code for token with code: ${code}`);
      const response = await axios.post(
        `http://127.0.0.1:5000/oauth/${brand}/callback`,
        { code }
      );
      return response.data;
    } catch (error) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
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
    const token = queryParams.get("token");

    if (token) {
      console.log(`Token received: ${token}`);
      localStorage.setItem("token", token);
      navigate("/home");
    } else {
      const code = queryParams.get("code");
      if (code) {
        mutation.mutate(code);
      }
    }
  }, [location.search, mutation, navigate]);

  const handleAuthClick = () => {
    console.log(`Redirecting to OAuth login for ${brand}`);
    window.location.href = `http://127.0.0.1:5000/oauth/${brand}/login`;
  };

  return { handleAuthClick, loading, error };
};

export default useAuth;
