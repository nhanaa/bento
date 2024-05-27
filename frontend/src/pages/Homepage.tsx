import React, { useState } from "react";
import Weather from "../components/homepage/TimeAndWeather";
import { FolderCardProps } from "@/lib/types";
import { mockFolders } from "@/lib/mocks";
import { FolderCard } from "@/components/homepage/FolderCard";
import { AddFolderCard } from "@/components/homepage/AddFolderCard";
import Layout from "./Layout";

const Homepage: React.FC = () => {
  const [folders, setFolders] = useState<FolderCardProps[]>(mockFolders);
  return (
    <Layout>
      <div className="h-1/2 flex flex-col justify-center items-center gap-5 p-10">
        <h1 className="font-bold ">Hello Pax!</h1>
        <Weather />
      </div>
      <div className="w-screen h-1/2 bg-gray-50 border-t border-gray-200">
        <div className="justify-center w-screen flex flex-wrap p-5 gap-2">
          {folders.map((folder, index) => (
            <FolderCard key={index} {...folder} />
          ))}
          <AddFolderCard
            triggerProps={
              "w-1/5 gap-5 flex items-center flex-wrap p-4 rounded-xl transition-colors hover:bg-gray-100 text-gray-500 border border-gray-200"
            }
          />
        </div>
      </div>
    </Layout>
  );
};



export default Homepage;
