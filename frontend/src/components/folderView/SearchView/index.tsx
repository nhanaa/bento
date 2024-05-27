import React from "react";
import { Accordion } from "./Accordion";
import { Searchbar } from "./Searchbar";

export const SearchView: React.FC = ({ items }) => {
  function filterContent(query: string) {
    return items.filter((item) => item.type === query);
  }

  return (
    <div className="w-1/3 h-full rounded-xl bg-gray-50 border border-gray-200 p-4 overflow-y-scroll">
      <Searchbar />
      <div className="flex flex-col w-full gap-1 p-2">
        <Accordion emoji="🔗" name="Links" content={filterContent("link")} />
        <Accordion emoji="📁" name="Files" content={filterContent("file")} />
        <Accordion
          emoji="🗾"
          name="Screenshots"
          content={filterContent("screenshot")}
        />
      </div>
    </div>
  );
};
