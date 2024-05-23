import React, { useState } from "react";
import Weather from "../components/homepage/TimeAndWeather";
import { FolderCardProps } from "@/lib/types";
import { mockFolders } from "@/lib/mocks";
import { FolderCard } from "@/components/homepage/FolderCard";
import { AddFolderCard } from "@/components/homepage/AddFolderCard";

const Homepage: React.FC = () => {
  const [folders, setFolders] = useState<FolderCardProps[]>(mockFolders);
  return (
    <div className="h-screen w-screen">
      <div className="h-1/2 flex flex-col justify-center items-center gap-5 p-10">
        <h1 className="font-bold ">Hello Pax!</h1>
        <Weather />
      </div>
      <div className="w-screen h-1/2 bg-gray-50 border-t border-gray-200">
        <div className="justify-center w-screen flex flex-wrap p-5 gap-2">
          {folders.map((folder, index) => (
            <FolderCard key={index} {...folder} />
          ))}
          <AddFolderCard />
        </div>
      </div>
    </div>
  );
};

export default Homepage;
