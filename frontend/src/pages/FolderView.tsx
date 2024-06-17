import React from "react";
import { useParams } from "react-router-dom";
import Layout from "./Layout";
import { Header } from "@/components/folderView/Header";
import { SummaryView } from "@/components/folderView/SummaryView";
import { SearchView } from "@/components/folderView/SearchView";
import { getFolder } from "@/hooks/useFolder";
import { Skeleton } from "@/components/ui/skeleton";

interface FolderParams {
  folderId: string;
}

const FolderView: React.FC = () => {
  const { folderId } = useParams<FolderParams>();
  const { data: folder, isLoading, isError, error } = getFolder(folderId ?? "");

  if (isLoading) {
    return (
      <Layout>
        <div className="flex w-full h-full flex-col gap-5 p-10">
          <Skeleton />
          <Skeleton />
          <Skeleton />
        </div>
      </Layout>
    );
  }

  if (isError) {
    return (
      <Layout>
        <div className="flex w-full h-full flex-col gap-5 p-10">
          <p className="text-red-500 text-sm">
            {error?.message || "Error loading folder."}
          </p>
        </div>
      </Layout>
    );
  }

  if (!folder) {
    return (
      <Layout>
        <div className="flex w-full h-full flex-col gap-5 p-10">
          <p className="text-red-500 text-sm">Folder not found.</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="flex w-full h-full flex-col gap-5 p-10">
        <Header emoji={folder.emoji} name={folder.name} />
        <div className="flex w-full h-5/6 flex-wrap justify-between">
          <SummaryView description={folder.summary} />
          {/* <SearchView
            web_urls={folder.web_url}
            download_urls={folder.download_urls}
            image_urls={folder.image_urls}
          /> */}
        </div>
      </div>
    </Layout>
  );
};

export default FolderView;
