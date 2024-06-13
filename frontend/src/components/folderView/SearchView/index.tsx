import React from "react";
import { Accordion } from "./Accordion";
import { Searchbar } from "./Searchbar";
import { Separator } from "@/components/ui/separator";

export const SearchView: React.FC = ({
  web_urls,
  image_urls,
  download_urls,
}) => {
  return (
    <div className="w-1/3 h-full rounded-xl bg-gray-50 border border-gray-200 p-4 overflow-y-scroll">
      <Searchbar />
      <div className="flex flex-col w-full gap-1 p-2">
        <Accordion emoji="🔗" name="Links" content={web_urls} />
        <Accordion emoji="📁" name="Files" content={download_urls} />
        <Accordion emoji="🗾" name="Screenshots" content={image_urls} />
      </div>
      <div className="justify-center px-2">
        <Separator className="bg-gray-200 my-5" />
      </div>
      {/* <div className="flex flex-col w-full gap-1 p-2">
        <Accordion
          emoji="👍"
          name="Recommended"
          content={filterContent("link")}
        />
      </div> */}
    </div>
  );
};
