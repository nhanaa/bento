import React, { useEffect, useState } from "react";
import Weather from "../components/homepage/TimeAndWeather";
import { FolderCardProps } from "@/lib/types";
import { FolderCard } from "@/components/homepage/FolderCard";
import { AddFolderCard } from "@/components/homepage/AddFolderCard";
import Layout from "./Layout";
import { useUser } from "@/contexts/UserContext";
import { getFolders } from "@/hooks/useFolder";
import { Skeleton } from "@/components/ui/skeleton";

const Homepage: React.FC = () => {
  const { user } = useUser();
  const {
    data: foldersData,
    isLoading,
    isError,
    error,
  } = getFolders(user?.id ?? "");
  const [folders, setFolders] = useState<FolderCardProps[]>([]);

  useEffect(() => {
    if (foldersData) {
      setFolders(foldersData);
    }
  }, [foldersData]);

  const getFirstName = (fullName: string): string => {
    return fullName.split(" ")[0];
  };
  return (
    <Layout>
      <div className="h-1/2 flex flex-col justify-center items-center gap-5 p-10">
        <h1 className="font-bold ">
          Hello {user && getFirstName(user["name"])}!
        </h1>
        <Weather />
      </div>
      <div className="w-screen h-1/2 bg-gray-50 border-t border-gray-200">
        <div className="justify-center w-screen flex flex-wrap p-5 gap-2">
          {isLoading ? (
            <Skeleton className="h-[125px] w-1/5 rounded-xl" />
          ) : (
            <>
              {folders.map((folder, index) => (
                <FolderCard key={index} {...folder} />
              ))}
            </>
          )}
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
