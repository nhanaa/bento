import React, { useState, ReactNode } from "react";
import { Sidebar } from "@/components/Sidebar";

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="h-screen w-screen">
      <Sidebar />
      {children}
    </div>
  );
};

export default Layout;
