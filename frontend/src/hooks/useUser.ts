import { useState } from "react";
import axios from "axios";

const useFetchUserIdByEmail = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getUserIdByEmail = async (email: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/users/email/${email}`);
      return response.data._id;
    } catch (error) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { getUserIdByEmail, loading, error };
};

export default useFetchUserIdByEmail;
