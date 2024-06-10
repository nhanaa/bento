import { useQuery } from 'react-query';
import axios from 'axios';

interface Folder {
  id: string;
  name: string;
  // Add other folder fields as needed
}

const fetchFoldersByUserId = async (userId: string): Promise<Folder[]> => {
  const response = await axios.get<Folder[]>(`http://127.0.0.1:5000/folders/${userId}`);
  return response.data;
};

export const useFolders = (userId: string) => {
  return useQuery(['folders', userId], () => fetchFoldersByUserId(userId), {
    enabled: !!userId, 
  });
};
