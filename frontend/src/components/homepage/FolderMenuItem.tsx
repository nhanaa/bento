import { FolderCardProps } from "@/lib/types";
import { FolderContextMenu } from "./FolderContextMenu";

export const FolderMenuItem = ({ emoji, name }: FolderCardProps) => {
  return (
    <div className="group w-full justify-between flex items-center flex-wrap p-4 rounded-xl bg-white transition-colors hover:bg-gray-100">
      <div className="flex flex-row gap-5">
        <h4>{emoji}</h4>
        <h4 className="truncate text-gray-700 font-medium">{name}</h4>
      </div>
      <span className="opacity-0 group-hover:opacity-100">
        <FolderContextMenu />
      </span>
    </div>
  );
};
