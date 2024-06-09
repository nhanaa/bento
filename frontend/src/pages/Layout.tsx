import React, { useState, ReactNode } from "react";
import { FolderCardProps } from "@/lib/types";
import { mockFolders } from "@/lib/mocks";
import { Sidebar } from "@/components/Sidebar/index";

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [folders, setFolders] = useState<FolderCardProps[]>(mockFolders);
  return (
    <div className="h-screen w-screen">
      <Sidebar folders={folders} />
      {children}
    </div>
  );
};

export default Layout;
