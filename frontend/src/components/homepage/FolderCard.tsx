import { FolderCardProps } from "@/lib/types";
import { FolderContextMenu } from "./FolderContextMenu";

export const FolderCard = ({ emoji, name, link }: FolderCardProps) => {
  return (
    <div className="w-1/5 justify-between flex items-center flex-wrap p-4 rounded-xl shadow bg-white transition-colors hover:bg-gray-100 border border-gray-200">
      <div className="w-2/3 flex flex-wrap gap-5">
        <h4>{emoji}</h4>
        <h4 className="truncate text-gray-800 font-semibold">{name}</h4>
      </div>
      <FolderContextMenu />
    </div>
  );
};
