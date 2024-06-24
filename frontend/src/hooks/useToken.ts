import { useState } from "react";
import axios from "axios";
import { AuthResponse } from "@/lib/types";

const useExchangeCodeForToken = (brand: string) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const exchangeCodeForToken = async (code: string): Promise<AuthResponse> => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post<AuthResponse>(
        `http://127.0.0.1:5000/oauth/${brand}/callback`,
        { code }
      );
      return response.data;
    } catch (error: any) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { exchangeCodeForToken, loading, error };
};

export default useExchangeCodeForToken;
