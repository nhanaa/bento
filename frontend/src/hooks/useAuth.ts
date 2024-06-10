import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useMutation, useQueryClient } from "react-query";
import axios from "axios";
import { useUser } from "../contexts/UserContext";

interface AuthResponse {
  email: string;
  token: string;
  name: string; 
}

const useAuth = (brand: string) => {
  const location = useLocation();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { setUser } = useUser();

  const exchangeCodeForToken = async (code: string): Promise<AuthResponse> => {
    setLoading(true);
    setError(null);
    try {
      console.log(`Exchanging code for token with code: ${code}`);
      const response = await axios.post<AuthResponse>(
        `http://127.0.0.1:5000/oauth/${brand}/callback`,
        { code }
      );
      console.log(response)
      return response.data;
    } catch (error: any) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const mutation = useMutation(exchangeCodeForToken, {
    onSuccess: (data) => {
      console.log(`data: ${data}`)
      console.log(`Token received: ${data.token}`);
      
      localStorage.setItem("token", data.token);
      setUser({ email: data.email, token: data.token, name: data.name }); // Ensure you set all user info
      queryClient.invalidateQueries(['user', data.email]);
      navigate("/home");
    },
    onError: (error: any) => {
      console.error("Error exchanging code for token:", error);
    },
  });

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get("token");
    const userInfo = queryParams.get("user");

    if (token && userInfo) {
      console.log(`Token received: ${token}`);
      localStorage.setItem("token", token);
      setUser(JSON.parse(decodeURIComponent(userInfo)));
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
