export type FolderCardProps = {
  emoji?: string;
  name: string;
  _id: string;
  noMenu?: boolean;
};


export interface User {
  email: string;
  name: string;
  id: string;
  token: string;
  login: boolean;
}

export interface UserContextType {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

export interface AuthResponse {
  email: string;
  token: string;
  name: string; 
}

export interface Folder {
  _id: string;
  emoji?: string;
  name: string;
  summary: string;
  user_id: string;
  web_urls: string[];
  download_urls: string[];
  image_urls: string[];
}

export interface AddFolderData {
  user_id: string;
  name: string;
  summary: string;
}

export type ContentType = {
  type: string;
  props: {
    level: number;
  };
  content: string;
};


export type Metadata =  {
  title: string;
  description: string;
  image: string;
}