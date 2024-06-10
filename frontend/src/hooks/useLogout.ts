import { useNavigate } from "react-router-dom";
import axios from "axios";

const useLogout = () => {
  const navigate = useNavigate();

  const logout = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/oauth/logout');
      console.log("logged out successfully!");
      localStorage.removeItem("token");
      navigate("/");
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return { logout };
};

export default useLogout;
