import { UseMutationResult, useMutation, useQuery } from 'react-query';
import axios from 'axios';
import { AddFolderData, Folder } from '@/lib/types';

const fetchFoldersByUserId = async (userId: string): Promise<Folder[]> => {
  const response = await axios.get<Folder[]>(`http://127.0.0.1:5000/folders/all/${userId}`);
  const folders = response.data.map(folder => {
    const [emoji, ...nameParts] = folder.name.split('_');
    const name = nameParts.join('_'); 
    return {
      ...folder,
      emoji,
      name,
    };
  });

  return folders;
};

const createFolder = async (data: AddFolderData): Promise<Folder> => {
  console.log(data);
  const response = await axios.post<Folder>('http://127.0.0.1:5000/folders', data);
  return response.data;
}

const fetchFolderById = async (id: string): Promise<Folder> => {
  const response = await axios.get<Folder>(`http://127.0.0.1:5000/folders/${id}`);
  const folder = response.data;
  const [emoji, ...nameParts] = folder.name.split('_');
  const name = nameParts.join('_'); 

  return {
    ...folder,
    emoji,
    name,
  };
};


export const getFolder = (folderId: string) => {
  return useQuery(['folder', folderId], () => fetchFolderById(folderId), {
    enabled: !!folderId,
    retry: false,
    onError: (error) => {
      console.error('Error fetching folder:', error);
    },
  });
};

export const getFolders = (userId: string) => {
  return useQuery(['folders', userId], () => fetchFoldersByUserId(userId), {
    enabled: !!userId, 
    retry: false,
    onError: (error) => {
      console.error('Error fetching folders:', error);
    },
  });
};

export const addFolder = (): UseMutationResult<Folder, Error, AddFolderData> => {
  return useMutation(createFolder, {
    onError: (error) => {
      console.error('Error creating folder:', error);
    },
  });
};

