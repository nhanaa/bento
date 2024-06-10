import { FolderCardProps } from "@/lib/types";
import { AddFolderCard } from "../homepage/AddFolderCard";
import { FolderMenuItem } from "../homepage/FolderMenuItem";

interface SidebarProps {
  folders: FolderCardProps[];
}

export const FolderMenu: React.FC<SidebarProps> = ({ folders }) => {
  return (
    <div className="flex flex-col">
      <div className="group flex flex-row justify-between items-center rounded-xl px-1 transition-colors hover:bg-gray-100">
        <p className="font-semibold text-sm text-gray-400">Folders</p>
        <AddFolderCard
          triggerProps={
            "scale-75 p-1 text-gray-500 justify-center rounded-xl opacity-0 group-hover:opacity-100 transition-opacity transition-colors hover:bg-gray-200"
          }
          textHidden={true}
        />
      </div>
      <div className="h-full w-full">
        <div className="justify-center w-full flex flex-col">
          {folders.map((folder, index) => (
            <FolderMenuItem key={index} {...folder} />
          ))}
        </div>
      </div>
    </div>
  );
};