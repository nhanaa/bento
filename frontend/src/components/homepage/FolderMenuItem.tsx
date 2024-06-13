import { FolderCardProps } from "@/lib/types";
import { FolderContextMenu } from "./FolderContextMenu";
import { useNavigate } from "react-router-dom";

export const FolderMenuItem = ({
  emoji,
  name,
  _id,
  noMenu = false,
}: FolderCardProps) => {
    const navigate = useNavigate();

    const handleClick = () => {
      navigate(`/folder/${_id}`);
    };
  return (
    <div onClick={handleClick} className="group w-full justify-between flex items-center flex-wrap p-4 rounded-xl bg-white transition-colors hover:bg-gray-100 active:bg-gray-100">
      <div className="flex flex-wrap gap-5">
        <h4>{emoji}</h4>
        <h4 className="truncate text-gray-700 font-medium">{name}</h4>
      </div>
      <span className="opacity-0 transition-opacity group-hover:opacity-100">
        {!noMenu && <FolderContextMenu />}
      </span>
    </div>
  );
};
