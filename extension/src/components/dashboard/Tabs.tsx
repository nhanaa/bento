import { Folders, UserRound } from "lucide-react";
import React from "react";
import { Tab } from "./Tab";

interface TabsProps {
  tab: string;
  setTab: (tab: "folders" | "settings") => void;
}

export const Tabs = ({ tab, setTab }: TabsProps) => {
  return (
    <div className="relative bottom-0 w-full flex space-x-1 mt-2">
      <Tab
        isActive={tab === "folders"}
        onClick={() => setTab("folders")}
        icon={<Folders className="w-6 h-6 text-customViolet" />}
      />
      <Tab
        isActive={tab === "settings"}
        onClick={() => setTab("settings")}
        icon={<UserRound className="w-6 h-6 text-customViolet" />}
      />
    </div>
  );
};
