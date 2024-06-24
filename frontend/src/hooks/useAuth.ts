import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useQueryClient } from "react-query";
import { useUser } from "../contexts/UserContext";
import useFetchUserIdByEmail from "./useUser";
import useExchangeCodeForToken from "./useToken";

const useAuth = (brand: string) => {
  const location = useLocation();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { setUser } = useUser();
  const { exchangeCodeForToken, loading: tokenLoading, error: tokenError } = useExchangeCodeForToken(brand);
  const { getUserIdByEmail, loading: userIdLoading, error: userIdError } = useFetchUserIdByEmail();

  useEffect(() => {
    const handleAuth = async () => {
      const queryParams = new URLSearchParams(location.search);
      const token = queryParams.get("token");
      const userInfo = queryParams.get("user");

      if (token && userInfo) {
        console.log(userInfo);
        localStorage.setItem("token", token);
        const data = JSON.parse(decodeURIComponent(userInfo));
        try {
          const userId = await getUserIdByEmail(data.email);
          setUser({ email: data.email, token: data.token, name: data.name, id: userId, login: true });
          navigate("/home");
        } catch (error) {
          console.error("Error fetching user ID by email:", error);
        }
      } else {
        const code = queryParams.get("code");
        if (code) {
          try {
            const data = await exchangeCodeForToken(code);
            localStorage.setItem("token", data.token);
            const userId = await getUserIdByEmail(data.email);
            setUser({ email: data.email, token: data.token, name: data.name, id: userId, login: true });
            queryClient.invalidateQueries(['user', data.email]);
            navigate("/home");
          } catch (error) {
            console.error("Error during authentication process:", error);
          }
        }
      }
    };

    handleAuth();
  }, [location.search, navigate, setUser, exchangeCodeForToken, getUserIdByEmail, queryClient]);

  const handleAuthClick = () => {
    window.location.href = `http://127.0.0.1:5000/oauth/${brand}/login`;
  };

  return { handleAuthClick, loading: tokenLoading || userIdLoading, error: tokenError || userIdError };
};

export default useAuth;
