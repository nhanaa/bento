import { Metadata } from "@/lib/types";
import axios from "axios";
import { useQuery } from "react-query";

const getMetadata = async (url: string): Promise<Metadata> => {
  const response = await axios.get<Metadata>(`http://127.0.0.1:5000/scrape?url=${encodeURIComponent(url)}`);
  return response.data;
};

export const getWebMetadata = (url: string) => {
  return useQuery(['scrape', url], () => getMetadata(url), {
    enabled: !!url, 
    retry: false,
    onError: (error) => {
      console.error('Error fetching metadata:', error);
    },
  });
};
