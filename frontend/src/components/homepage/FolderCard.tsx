import { FolderCardProps } from "@/lib/types";
import { FolderContextMenu } from "./FolderContextMenu";

export const FolderCard = ({ emoji, name, link }: FolderCardProps) => {
  return (
    <div className="w-1/5 justify-between flex items-center flex-wrap p-4 rounded-xl shadow bg-white transition-colors hover:bg-gray-100 border border-gray-200">
      <h4>{emoji}</h4>
      <h4 className="truncate text-gray-800 font-semibold">{name}</h4>
      <FolderContextMenu />
    </div>
  );
};
